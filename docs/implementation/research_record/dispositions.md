---
status: living
created: 2026-08-14
updated: 2026-08-14
---

# Prompt-corpus disposition table — every prompt in the ≥ 150-word band, triaged

**Stage 1 of [`../../handoffs/2026-08-06_research_record_from_prompt_corpus.md`](../../handoffs/2026-08-06_research_record_from_prompt_corpus.md), run 2026-08-14.**
The corpus is the **uuid-deduplicated union of the 2026-08-08 and 2026-08-14 snapshots**
(`~/mtdsim-corpus-snapshot/`): 107 prompts / 79 698 words. The union matters because the
live store keeps losing transcripts — 14 of these prompts now exist *only* in the
2026-08-08 snapshot (July's ≥ 150-word band fell 47 → 33 in the live store between the
two snapshots). Every row was read in full, in chronological order.

**Bands** (from the brief): 1 direction-setting · 2 design rationale · 3 implementation
constraint · 4 evaluation intent · 5 abandonment/reversal · 6 methodological correction ·
7 noise.
**Dispositions:** `already-recorded` (cite in summary) · `record-drifted` (see § flags) ·
`annal-entry` (→ thread file) · `note-candidate` (→ Stage 3) · `noise`.
**Threads** map to the files in [`threads/`](threads/). Summaries are paraphrase — never
verbatim third-party text; the verbatim source is the untracked snapshot, keyed by uuid.

May and June 2026 have **zero transcripts** against 92 `dev` commits — that window was
introduction and literature-review work, out of this record's scope. A boundary, not a loss.

| # | Date | Words | uuid | Branch | B | Disposition | Thread | Summary |
|---|------|-------|------|--------|---|-------------|--------|---------|
| 0 | 2026-04-19 | 333 | `e000275d` | `feat/attacker-profiling` | 7 | annal-entry | VIZ | GAP visualiser UX fixes; drop APT-group 'motivation' chips — first signal of the objective pivot |
| 1 | 2026-04-19 | 445 | `1c45f517` | `feat/attacker-profiling` | 7 | annal-entry | VIZ | More visualiser UX; MITRE provenance links; consensus-edges legacy removed (Attack-Flow priority) |
| 2 | 2026-04-22 | 2967 | `a0dc6371` | `feat/attacker-profiling` | 2 | annal-entry | INT | Demo-day plan: wrap-not-modify profile, legacy bit-identity acceptance test, event-log contract, DDQN untouched |
| 3 | 2026-04-22 | 156 | `10924b69` | `feat/attacker-profiling` | 7 | noise | — | Notebook run harness, progress bar |
| 4 | 2026-04-22 | 207 | `43338671` | `feat/attacker-profiling` | 3 | annal-entry | BUG | Same harness; first sighting of the long-run hang ('there still exists a hang somewhere') — later the silent integrity failure |
| 5 | 2026-04-23 | 1875 | `f0c00c00` | `feat/replay-viz` | 2 | annal-entry | VIZ | Situational-awareness visualiser checklist (six layers incl. IDS/POMDP stretch) — the programme later dropped whole |
| 6 | 2026-04-23 | 1245 | `340bc4a9` | `feat/replay-viz` | 7 | annal-entry | VIZ | Replay visualiser core-flow critique; Tay parameters as configurable presets |
| 7 | 2026-07-09 | 216 | `0fc8a125` | `dev` | 2 | annal-entry | TIM | Tactic-profiling defence section commissioned as prospective justification for the declared durations — argue before building |
| 8 | 2026-07-09 | 193 | `7a713d92` | `dev` | 6 | already-recorded | RQ | Draft defence critiqued: decouple from internal rubric, write for a CS-honours reader → the reader contract (notes_rubric.md, voice.md) |
| 9 | 2026-07-10 | 490 | `2ceb2fcd` | `dev` | 2 | already-recorded | TIM | Supervisor questions: calibration overfitting, 'weak validation power', finite timeline vs FSM cycling, gains MTD cannot deny (operational_validation.md; state_bounds_measurable_disruption.md) |
| 10 | 2026-07-10 | 498 | `1b4e72df` | `dev` | 2 | already-recorded | TIM | Question set refined: calibration / coupling / success-failure encoding themes (operational_validation.md) |
| 11 | 2026-07-10 | 357 | `b4074eaa` | `dev` | 1 | already-recorded | OBJ | L0–L5 pipeline summary; Claude-derived classification flagged as needing verification (gasp_schema.md §(c) audit trail) |
| 12 | 2026-07-13 | 877 | `daf312df` | `dev` | 6 | already-recorded | RQ | Docs-refactor charter: two-consumer principle, rubric-gated chapter-keyed notes (docs_map.md, notes_rubric.md) |
| 13 | 2026-07-13 | 2598 | `0220a3af` | `chore/docs-refactor` | 1 | annal-entry | OBJ | 23-Jun update + 25-Jun minutes metabolised: attacker-only scope, sparse-corpus acceptance, justified durations, v1 decoupled run; visualiser + process-mining dropped; group→objective pivot |
| 14 | 2026-07-13 | 8983 | `b31cf4fa` | `chore/docs-refactor` | 7 | already-recorded | RQ | Dissertation-writing lecture transcript → _writing_guide.md (provenance in its frontmatter) |
| 15 | 2026-07-13 | 1628 | `9dec99c3` | `dev` | 1 | annal-entry | TIM | 10-Jul update: pipeline before calibration; recon-as-parameter idea; per-objective termination criteria; timing advice received |
| 16 | 2026-07-13 | 647 | `c9916dff` | `dev` | 2 | note-candidate | SEAM | Binding charter: trivial petri→CKC mapping 'yields no meaningful results'; Caldera rejected as too bulky; insight-over-attacker-strength values statement |
| 17 | 2026-07-13 | 199 | `128d1c34` | `dev` | 6 | annal-entry | CMP | Correction: 1:1 comparability to Zhang/Tay is not a dealbreaker — 'simulation settings can be updated to suit the experiments' |
| 18 | 2026-07-13 | 867 | `58e41f7d` | `dev` | 7 | already-recorded | RQ | voice.md genesis (voice contract; out of this brief's scope) |
| 19 | 2026-07-13 | 215 | `301688b4` | `dev` | 7 | already-recorded | RQ | Lit-review examiner feedback folded into voice rules (memory + voice.md) |
| 20 | 2026-07-13 | 5562 | `a18a9748` | `dev` | 7 | already-recorded | RQ | Authored-prose forensic report integrated into voice.md evidence rules |
| 21 | 2026-07-14 | 1627 | `e0bccd0d` | `dev` | 1 | already-recorded | SEAM | Meeting agenda: CTI-ontology binding chain tactic→technique→CAPEC→CWE→CVE→CVSS and the real/synthetic barrier (structure_to_behaviour_binding.md) |
| 22 | 2026-07-14 | 223 | `0777500f` | `dev` | 7 | annal-entry | SEAM | Diagram ask: expose the synthetic/real vulnerability boundary as an unbiased conversation aid |
| 23 | 2026-07-15 | 7483 | `ef064e1e` | `dev` | 1 | already-recorded | SEAM | 15-Jul meeting bundle (third-party transcript): binding, action-set, profile-shape rulings → that week's handoffs |
| 24 | 2026-07-16 | 401 | `326d96ba` | `dev` | 2 | note-candidate | SEAM | Movement/controller/action trichotomy coined; controller as 'the best we can do with the tools at hand'; predicts movement attacker performs at-or-below baseline |
| 25 | 2026-07-21 | 486 | `1ccaf7fe` | `dev` | 2 | annal-entry | SEAM | Pipeline diagram: movement stack, controller as substitutable join — 'two independent components which can be subbed in or out' |
| 26 | 2026-07-21 | 211 | `6a0522e0` | `dev` | 4 | annal-entry | RQ | First-experiment write-up structure for the supervisor update |
| 27 | 2026-07-21 | 250 | `cb2aacb4` | `dev` | 2 | note-candidate | OVL | Success/failure binary tactic-pair weighting genesis — ordering implicit in the two dictionaries, CKC layering dropped |
| 28 | 2026-07-21 | 363 | `bd5e2cca` | `dev` | 2 | note-candidate | OVL | Overlay epistemics: CTI records successes, not failures; no reverse-engineering the nets; 'knowledge and real world data working together at runtime' |
| 29 | 2026-07-21 | 180 | `638190bb` | `dev` | 3 | annal-entry | SEAM | Controller mapping doubts: empty tactics, multi-phase mappings — parked as experiment-1 open questions |
| 30 | 2026-07-21 | 200 | `5a858095` | `dev` | 2 | annal-entry | OVL | Grounds-up weighting of the whole tactic-pair set; extensible action set; resource-dev added to overlay |
| 31 | 2026-07-22 | 266 | `4b086c3b` | `dev` | 2 | annal-entry | FAIR | Boundary understanding: should the defender manipulate attacker state directly or via network state? Timing conflict movement vs action layer named |
| 32 | 2026-07-22 | 208 | `994590be` | `dev` | 7 | annal-entry | SEAM | Data-flow diagram between movement layer and MTDSim components |
| 33 | 2026-07-23 | 218 | `b0ead01b` | `dev` | 2 | annal-entry | SEAM | Tactic×phase mapping table; action dependencies (precondition idea); ideal-form column |
| 34 | 2026-07-23 | 201 | `b0b0244f` | `dev` | 6 | note-candidate | OVL | Adversarial multi-agent scrutiny of overlay weights to 95 % confidence; a dedicated no-reverse-engineering bot |
| 35 | 2026-07-23 | 322 | `1d6b5644` | `dev` | 2 | already-recorded | SEAM | Runtime loop specified: token → controller dispatch → verdict → weight transform → next transition (architecture.md M1/M2) |
| 36 | 2026-07-23 | 242 | `d7d332e7` | `dev` | 4 | note-candidate | CMP | Experiment-1 framing: behaviour over outcome — 'not expecting the movement attacker to perform better'; quality over quantity |
| 37 | 2026-07-23 | 193 | `aa715c97` | `experiment/l3-first-numbers` | 4 | already-recorded | MOV | Experiment-1 reading in own words: rushed-phases stall vs unblocked-but-uncompromising; recon-heavy or exploit-empty (experiment_01_findings.md) |
| 38 | 2026-07-27 | 3245 | `46734f13` | `experiment/l3-first-numbers` | 1 | annal-entry | CRIT | Six-point metabolisation of 27-Jul meeting: weight sensitivity, action-set freeze, stochastic timing, mapping v2, sink retrace, criterion genesis — 'isn't promising the world' |
| 39 | 2026-07-27 | 277 | `66e97cfd` | `experiment/l3-first-numbers` | 7 | already-recorded | INT | main rebuilt as standalone simulator for the incoming student; deliberate dev/main divergence |
| 40 | 2026-07-27 | 263 | `344a01bc` | `docs/lifecycle-consensus-overlay` | 6 | already-recorded | BUG | Bug rulings against brown2023; fix-verified-bugs-only boundary (guardrails.md) |
| 41 | 2026-07-28 | 271 | `16cba0c8` | `dev` | 2 | annal-entry | CRIT | Axis walkthrough in own words; MTD-awareness as a [0,1] sensitivity dial idea; 'not looking to go into deep RL' |
| 42 | 2026-07-28 | 268 | `26b48719` | `dev` | 2 | note-candidate | TIM | GSPN as 'veneer over the inherently arbitrary'; portability argument keeps the confusion penalty on the simulator side of the border |
| 43 | 2026-07-28 | 202 | `05d7f270` | `dev` | 5 | already-recorded | TIM | S3-R reversal: substrate timings retired; the movement layer owns all attacker time (register S3-R) |
| 44 | 2026-07-28 | 156 | `091585b1` | `dev` | 2 | annal-entry | OVL | Weight-sensitivity intuition: persistence forbids far falls; recon→impact must be zero — distance-damped jumps |
| 45 | 2026-07-28 | 422 | `ba51a9d2` | `dev` | 2 | annal-entry | CRIT | Badge-raising push; stealth-state design sketched (never built); axis-8 marked future work — 'we will not be implementing this' |
| 46 | 2026-07-28 | 231 | `c066d3b0` | `dev` | 6 | note-candidate | BUG | Intent-spec genesis: 'is what you are fixing actually a bug' — literature-only spec, Brown primary, Zhang/Tay secondary |
| 47 | 2026-07-29 | 295 | `ec4c81ac` | `feat/axis7-learning-capability` | 6 | annal-entry | BUG | Verification anxiety: each model release finds more bugs; how can conformance to Brown's intent ever be complete? |
| 48 | 2026-07-29 | 260 | `4e874d98` | `feat/axis7-learning-capability` | 4 | annal-entry | CRIT | Experiment-2 brief: the eight axes as the lens; 'plainly explain' the hiccups |
| 49 | 2026-07-29 | 379 | `95096177` | `feat/axis134-demonstration-arms` | 2 | annal-entry | LRN | Learning as natural adaptation to whatever substrate shape — the portability framing of the learner |
| 50 | 2026-07-29 | 220 | `1dcc8b71` | `feat/axis134-demonstration-arms` | 2 | annal-entry | INC | No costs in the GSPN; attacker-gives-up idea after X thwarted attempts — the disengagement seed |
| 51 | 2026-07-29 | 316 | `11efe5e7` | `feat/axis134-demonstration-arms` | 2 | annal-entry | LRN | Fact-set bridge mused; learning-to-match-baseline framing — reversed in the next prompt |
| 52 | 2026-07-29 | 230 | `eeb0ad0e` | `feat/axis134-demonstration-arms` | 5 | note-candidate | CMP | Census reframe: measure qualities the baseline cannot demonstrate; baseline stands in for the field's attacker models — 'break the framing that we are comparing' |
| 53 | 2026-07-29 | 228 | `391ceb8c` | `feat/axis134-demonstration-arms` | 1 | note-candidate | CMP | Attack model as means, not end; extensibility claim (port to your simulator, tactic → technique level); criterion is an instrument |
| 54 | 2026-08-01 | 872 | `637e176f` | `perf/mtd-mechanism-cost-audit` | 1 | note-candidate | MOV | Freeze acceptance: the FSM is the weakest link; at-best-par expectation; 'no embellishing with half-cooked implementations' |
| 55 | 2026-08-01 | 343 | `9e3b486f` | `docs/model-freeze-and-unification` | 2 | annal-entry | CRIT | Own plain-language definitions of all eight axes — the vocabulary later used to the supervisor |
| 56 | 2026-08-01 | 360 | `2d0838e0` | `docs/model-freeze-and-unification` | 1 | annal-entry | CRIT | Direction consolidation: learning generalisation, incentive simplification, stealth-as-tempo, disengagement/downtime balance |
| 57 | 2026-08-01 | 167 | `9a37231d` | `feat/learning-procedural-rigidity` | 2 | already-recorded | INC | 'There is nothing the attacker can reason about' — the missing-utility diagnosis (criterion axis 6 final disposition) |
| 58 | 2026-08-01 | 281 | `7ba2f3cf` | `feat/learning-procedural-rigidity` | 2 | annal-entry | INC | Incentive as opportunity cost across networks; the three run outcomes; what is attack utility? |
| 59 | 2026-08-01 | 162 | `c8008b7f` | `feat/learning-procedural-rigidity` | 2 | already-recorded | INC | 'MTD is a progress-destroying exercise; rationality is progress/effort' (attacker_disengagement.md) |
| 60 | 2026-08-02 | 205 | `4a2c7535` | `feat/iterated-cost-model` | 2 | annal-entry | INC | Progress/effort enumeration via independent-subagent rubric method — design and cross-examination separated |
| 61 | 2026-08-02 | 607 | `eedf71d2` | `feat/iterated-cost-model` | 6 | annal-entry | LRN | Self-mining ask (precedent for this record); learning-thread consolidation; workflow-chains-not-RL disagreement |
| 62 | 2026-08-02 | 307 | `36e1e36e` | `chore/os-service-diversity-classification` | 2 | annal-entry | LRN | Progress = shortest path to legal phases — explicitly a controller-layer proxy, not generalisable, and owned as such |
| 63 | 2026-08-02 | 414 | `510c78c2` | `chore/os-service-diversity-classification` | 2 | note-candidate | FAIR | Boundary programme genesis: fair/faithful integration at three seams 'for a fair contest'; 95 % confidence A/B loop |
| 64 | 2026-08-02 | 169 | `fba98584` | `chore/boundary-network-defender-review` | 5 | already-recorded | INC | Incentive resolved as metric-only: disengagement when cost exceeds threshold (criterion axis 6; disengagement record) |
| 65 | 2026-08-03 | 150 | `1543ffe7` | `chore/boundary-network-defender-review` | 3 | annal-entry | SEAM | Alignment-dial path rules: dwell-only intermediates, reachable-verb candidates, time-agnostic |
| 66 | 2026-08-03 | 154 | `1df50f8b` | `chore/boundary-network-defender-review` | 3 | annal-entry | SEAM | Alignment dial as float [0,1] — a tunable concession to inherited rigidity, 'the facade of strategic pluralism' preserved |
| 67 | 2026-08-04 | 3144 | `2568d33c` | `chore/boundary-network-defender-review` | 1 | already-recorded | CRIT | 4-Aug meeting (third-party): stealth via tempo and network metrics, CVSS-derived detection idea, disruption uniformity (minutes + register) |
| 68 | 2026-08-05 | 430 | `db759173` | `chore/boundary-network-defender-review` | 1 | annal-entry | FAIR | Disruption uniformity resolution; handoff consolidation; vulnerability-memory/swift-mode floated as axis-8 PoC |
| 69 | 2026-08-06 | 931 | `2136c3af` | `feat/stealth-exposure-reader` | 6 | already-recorded | RQ | This mining brief's genesis: prompts are the record of intent; output is an execution layer |
| 70 | 2026-08-06 | 267 | `94a01c3b` | `chore/gasp-class-rename` | 2 | annal-entry | AX8 | Smart-APT unification vision: vulnerability memory + detectability-as-loss-function + opportune-time exploitation |
| 71 | 2026-08-06 | 168 | `eae73f5f` | `chore/gasp-class-rename` | 2 | annal-entry | AX8 | Rationality around exploit success and detectability; swift-mode as measured characteristic |
| 72 | 2026-08-06 | 373 | `386aac75` | `dev` | 2 | annal-entry | AX8 | Side-channel premise: attacker deduces MTD decision boundaries from the metrics; Tay retrain contemplated |
| 73 | 2026-08-07 | 225 | `41eebd7a` | `chore/knowledge-gated-prereq-checks` | 3 | annal-entry | AX8 | Tay weights archive doubted: improperly trained, non-standard hyperparameters; Kaya retrain offered |
| 74 | 2026-08-07 | 179 | `f9408c2c` | `chore/knowledge-gated-prereq-checks` | 3 | annal-entry | AX8 | Reward-function hunt in Tay's paper; downtime/operational-impact needed; 95 % confidence before any retrain |
| 75 | 2026-08-07 | 167 | `733c86a8` | `chore/mtd-ai-forensics` | 2 | annal-entry | LRN | Exploit-learning signal encoded at the exploit verb; no petri jumps allowed; stealth 'emerges as measurement' |
| 76 | 2026-08-08 | 194 | `35f9de20` | `feat/mtd-ai-cost-calibrated` | 2 | annal-entry | AX8 | Axis-8 design: act below the no-op decision boundary, strike when confident |
| 77 | 2026-08-09 | 439 | `4930d056` | `dev` | 1 | annal-entry | CRIT | 9-Aug update in own words: axis table; axis 8 killed — 'calibration defeats the purpose'; axis 4 renamed 'strategic robustness' in his framing |
| 78 | 2026-08-09 | 158 | `149e5bee` | `viz/plurality-reporting` | 2 | already-recorded | CRIT | Persistence has no contrast class — 'comparing against nothing' (persistence_duration_premise.md) |
| 79 | 2026-08-09 | 158 | `4dc2a9e4` | `viz/plurality-reporting` | 7 | noise | — | Duplicate of #78 (same prompt, second session) |
| 80 | 2026-08-09 | 153 | `8c35ffd7` | `feat/plural-preference-instrumentation` | 2 | annal-entry | CRIT | Axis-4 dissertation framing: plural recovery from failure; shipped instruments don't appreciate the framing |
| 81 | 2026-08-10 | 214 | `1a9ba351` | `dev` | 4 | note-candidate | CMP | Behaviour-composition metric ask: baseline has one behaviour; 'a well thought out metric that returns a negative result' over slop → effective behavioural breadth |
| 82 | 2026-08-10 | 261 | `2c4a6dcb` | `docs/predictability-handoff` | 1 | already-recorded | RQ | Methodology skeleton + supervisor's simplification (third-party feedback) (dissertation.tex, register) |
| 83 | 2026-08-10 | 261 | `a33cf29d` | `dev` | 7 | noise | — | Duplicate of #82 |
| 84 | 2026-08-10 | 261 | `331f8a3b` | `dev` | 7 | noise | — | Duplicate of #82 |
| 85 | 2026-08-11 | 507 | `829113d6` | `dev` | 1 | annal-entry | RQ | Experimental-setup workshop: RQ nailing, sub-questions-as-criterion idea, grey-box design discipline |
| 86 | 2026-08-11 | 275 | `34facaac` | `dev` | 1 | annal-entry | RQ | Transparent rankings; 'sell up what we can justify'; lineage headlines become discussion comparison points |
| 87 | 2026-08-11 | 203 | `3963cf40` | `dev` | 6 | annal-entry | RQ | Structure feedback: barebones sections, two dimensions, anti-vacuous rule |
| 88 | 2026-08-11 | 235 | `8072276d` | `dev` | 4 | annal-entry | LRN | Learning scale-dependence hypothesis: constrained service pool → pronounced exploit learning → diversity hit hardest (in flight) |
| 89 | 2026-08-11 | 235 | `c8b02538` | `dev` | 7 | noise | — | Duplicate of #88 |
| 90 | 2026-08-11 | 235 | `5707de9f` | `dev` | 2 | annal-entry | CRIT | Axis-4 framing restated for instrumentation; admits the shipped definition is simulator-tied |
| 91 | 2026-08-11 | 4730 | `5873a2c2` | `dev` | 1 | already-recorded | RQ | 11-Aug meeting (third-party transcript): V1–V7 — validation directive, RQ reframe, background chapter, MTD-AI used as-is, sensitivity regime (register) |
| 92 | 2026-08-11 | 4551 | `6a66c90e` | `dev` | 7 | noise | — | Same 11-Aug transcript pasted in a second session |
| 93 | 2026-08-11 | 862 | `25fbcc9e` | `feat/exploit-learning-mechanism` | 1 | already-recorded | RQ | Own minutes draft of V1–V7 for the register |
| 94 | 2026-08-11 | 195 | `dce5e294` | `feat/exploit-learning-mechanism` | 4 | annal-entry | INC | Disengagement sweep ask; axes 4 and 8 named recorded failures, pushed to future work |
| 95 | 2026-08-11 | 195 | `14089bb6` | `feat/exploit-learning-mechanism` | 7 | noise | — | Duplicate of #94 |
| 96 | 2026-08-11 | 184 | `5e99c916` | `feat/exploit-learning-mechanism` | 3 | annal-entry | LRN | Exploit-learning wiring debug: the impact gate supersedes the mechanism — 'ironically having no impact' |
| 97 | 2026-08-11 | 209 | `d757be1d` | `dev` | 2 | note-candidate | MOV | Movement-objectives diagnosis: verb decoupling never propagated to the general/targeted objectives; churn is the symptom |
| 98 | 2026-08-11 | 186 | `4a502548` | `dev` | 2 | annal-entry | MOV | Emergent-objective puzzle: the FSM-order-destroyed objective — reinstate it, or does the RQ even need it? |
| 99 | 2026-08-11 | 313 | `449f2d34` | `dev` | 1 | note-candidate | MOV | The concession drafted for the supervisor: weakest link, intrinsic incompetence under the freeze, extensibility as the answer — and the refusal to optimise toward the baseline |
| 100 | 2026-08-12 | 246 | `d3413042` | `docs/movement-objectives-design` | 1 | already-recorded | RQ | Whole-dissertation frame: intro/background/lit/method/results/discussion/future-work; capture–model–evaluate (writing guide, register V5) |
| 101 | 2026-08-12 | 194 | `80dc285b` | `docs/movement-objectives-design` | 1 | already-recorded | RQ | Chapter section lists ratified (dissertation.tex skeleton) |
| 102 | 2026-08-12 | 356 | `1154cc1b` | `docs/dissertation-skeleton-subquestions` | 6 | already-recorded | RQ | Unit-ledger genesis: 250-word units, ~60-unit budget (_writing_guide.md) |
| 103 | 2026-08-13 | 430 | `8fdda12e` | `dev` | 6 | already-recorded | RQ | Critique-protocol genesis: grey-box voice review (critique_protocol.md) |
| 104 | 2026-08-13 | 177 | `9ade0a40` | `dev` | 2 | annal-entry | CRIT | Axis-4 pivot-kernel frame proposed; axis-8 exploitability question → the structural probe and the declined kernel (criterion 2026-08-13) |
| 105 | 2026-08-13 | 1808 | `13377d02` | `dev` | 7 | noise | — | Pasted design-skill text for a visualisation session |
| 106 | 2026-08-14 | 303 | `73091bf9` | `dev` | 6 | annal-entry | RQ | This session's green-light: chapter remapping, mine the corpus into the notes |

## Record-drifted flags (collected; the one edit made is stated)

1. **`docs/notes/ch6_discussion/procedural_mismatch_artefact.md`** (written 2026-08-01)
   states the alignment instrument is "designed but not built". The instrument **was
   built** as the alignment dial (`src/mtdsim/l3_simulation/movement/alignment.py`,
   landed via `chore/boundary-network-defender-review`, 2026-08-03; prompts #65–66 are
   the build instruction). Because Marc's 2026-08-14 instruction licenses note edits in
   this session, the note's sentence was corrected and `updated` bumped in the Stage 3
   commit — recorded here so the flag and its action are both on the record.
2. **Chapter numbering across the writing scaffolding** (docs_map chapter table,
   `_writing_guide.md` one-line-job table, `session_workflow.md` examples) lagged the
   ratified structure (background before literature review; a future-work chapter;
   conclusion pushed to ch8). Fixed in the notes-restructure commit under the 2026-08-14
   instruction; the authority for the structure is the 2026-08-11 register (V-series) and
   prompt #101, not this record.
3. **No flag** on the axis-4 naming difference (prompts #77/#80/#90 call it "strategic
   robustness / plural recovery"; the criterion holds "adaptivity to defender
   resistance"): the criterion's 2026-08-11 and 2026-08-13 dispositions post-date those
   prompts, so the prompts are the superseded side. Recorded so a future reader does not
   raise it as drift. The *write-up framing* in those prompts remains available to the
   methodology chapter — that is a drafting choice, not a record conflict.

## Where the note-candidates went (Stage 3 mapping)

| Candidate rows | Note |
|---|---|
| 27, 28, 30, 34, 44 | `docs/notes/ch4_methods/outcome_overlay_directionality.md` (new) |
| 46, 47, 40, 4 | `docs/notes/ch4_methods/bug_or_design_verification.md` (new) |
| 52, 53, 36, 81, 99, 54 | `docs/notes/ch6_discussion/refusing_the_baseline_race.md` (new) |
| 54, 99, 104, 53 | `docs/notes/ch7_future_work/successor_programme.md` (new) |
| 16, 24, 42, 63, 97 | strengthened existing notes / thread files only — the arguments were already carried by `structure_to_behaviour_binding.md`, `host_simulator_contract.md`, the boundary records, and `procedural_mismatch_artefact.md`; a pointer beats a retelling |

## Short-band scan (75–150 words), 2026-08-14

Run in response to Marc's question whether argument hides below the ≥ 150-word cut.
The band holds **65 prompts / ~6 900 words** (union of both snapshots). The brief's
heuristic — long prompts carry the argument mass, short ones steer — held for the
bulk of it: most are logistics (handoff reads, retire/merge instructions, diagram
tweaks, confirmations). But it is not clean, and a dozen carry real argument. These
were read; the band was **not** given full per-prompt dispositions (out of the
brief's declared ≥ 150 scope), but the argument-bearing ones are recorded here, and
the one genuine gap was folded into a thread.

| Date | ~w | Argument | Action |
|---|---|---|---|
| 2026-08-01/02 | 142/91 | **Time-as-cost is the wrong input** — a time-denominated effort rewards fast attacks, against APT low-and-slow; the durations are themselves arbitrary. The *reasoning* behind the incentive thread's pivot. | **Folded** into [`threads/incentive_rationality.md`](threads/incentive_rationality.md) |
| 2026-07-29 | 95 | The thesis in one line: "what does greater attack fidelity imply on current evaluation methods of MTD" | Covered by [`threads/comparability_and_census.md`](threads/comparability_and_census.md) (#53); recorded here as its tightest phrasing |
| 2026-07-28 | 138 | Transparency demand on the overlay weighting — "surface your logic … it's not particularly transparent" | Methodological-correction instance; the pattern is in [`threads/outcome_overlay.md`](threads/outcome_overlay.md) |
| 2026-07-29 | 141 | Learning must **generalise to any FSM**, not just this substrate; penalty-only routing will not produce the ordering, memory chains will | Reinforces [`threads/learning_capability.md`](threads/learning_capability.md) |
| 2026-07-29 | 123 | Incentive via the targeted attacker — reuse Brown's general/targeted objective as the incentive channel | Covered by [`threads/incentive_rationality.md`](threads/incentive_rationality.md) |
| 2026-08-09 | 108 | **Variety is not strategic plurality** — variety is the capacity, plurality is the measure over it | Shaped the effective-behavioural-breadth metric; in the criterion axis 3 |
| 2026-08-06 | 100 | Discussion framing — APT as latent risk to under-moving networks; what/how/when to move as an optimisation | Candidate discussion/ch6 point; not yet a note |
| 2026-08-11 | 126 | Churn diagnosis — the movement attacker lacks the baseline's pivot, so it recompromises held hosts | Covered by [`threads/movement_objectives.md`](threads/movement_objectives.md) |
| 2026-08-12 | 136 | The capture/model/evaluate methodology section layout, worked in detail | Covered by [`threads/rq_and_structure.md`](threads/rq_and_structure.md) |

**Reading for the delta pass:** the short band is worth a proper triage only if the
second extraction (post-metrics) also lowers its floor; the ≥ 150 band remains the
primary corpus, and nothing here changes a disposition already recorded above. The
one substantive recovery — the time-as-cost objection — is now in the incentive
thread where it belongs.

### 15–75 band sanity check, 2026-08-14

Also swept, on Marc's ask, to confirm nothing was left on the table below 75 words.
**272 prompts / ~8 600 words**, averaging ~32 words — the floor of the corpus.
A regex for argument signals (`because`, `the goal`, `makes no sense`, `incentive`,
`fidelity`, `disagree`, …) over prompts ≥ 35 words flagged 42; each was read. The
band is what the brief predicted: clarifying questions, diagram-and-figure tweaks,
handoff reads, confirmations, and steering. The argument-bearing minority all resolve
into threads already written — the weakest-link/measured-negative framing
([`threads/comparability_and_census.md`](threads/comparability_and_census.md),
[`threads/movement_objectives.md`](threads/movement_objectives.md)); the
axis-3-vs-axis-4 vocabulary correction and the predictability-name retirement
([`threads/criterion_lifecycle.md`](threads/criterion_lifecycle.md)); the
build-in-baseline "validation by proxy" tactic (a facet of the learning and
comparability threads); the recurring human-oversight-of-headings anxiety
([`threads/rq_and_structure.md`](threads/rq_and_structure.md)). **No new decision,
reversal, or abandoned path surfaced below 75 words** that a thread does not already
own. The band does not warrant its own triage; recorded so it is not re-swept.
