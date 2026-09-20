# Extraction-only sources: evaluation design, sensitivity analysis, replication conventions

**STATUS: EXTRACTION-ONLY.** Every block below is read from the paraphrase-heavy
extraction records in `docs/sources/extractions/`. The primary papers' full text
is NOT in the repo (source files are gitignored or absent), so nothing here has
been verified against the primary. Line numbers are those of the extraction file
(`cat -n`). Where the extraction carries no information on a point the block
says "not in extraction". Extractions were dissected for tactic-profile /
MTD-interaction purposes (dwell, reset, sweep width), not for evaluation
methodology, so absence of evaluation detail in an extraction is NOT evidence of
absence in the paper.

Survey date: 2026-09-09. Survey scope: 12 extractions named in the brief, one
per pass, then a grep census across `docs/sources/`.

---

## 1. `evans2011_mtd_effectiveness.md` (127 lines)

**(a) Paper + citation line.** Evans, Nguyen-Tuong & Knight 2011, "Effectiveness
of Moving Target Defenses", Chapter 2 of the Springer *Moving Target Defense*
volume (Advances in Information Security 54), DOI
https://doi.org/10.1007/978-1-4614-0977-9_2 (L1, L3–4, L28–30). Pages cited:
Ch. 2 §2.3–2.6, pp. 33–46 (L30). Citation key `evans2011` (L28).

**(b) Evaluation design.** Analytical model, not an empirical simulation study:
two players, attacker knows a vulnerability, defender runs a key-dependent
transform re-randomised over time; `te` = time from exploit start to compromise;
an exploit constructed at t₁ fails if launched at t₂ after a re-randomisation
(L37–47). Evaluation is a per-attack-class taxonomy (circumvention / deputy /
brute-force / probing / incremental) with a qualitative verdict per class
(Table 2.1, L58–71). Network/scenario setup: not in extraction (the model is
memory-diversity, ASLR/ISR/data randomisation, not network shuffle — L114–119).
Replication counts: not in extraction (analytical). Metric: attack-success
probability and expected attack time (L96–103). Presentation: Table 2.1 and
Fig. 2.2 (L58, L94).

**(c) Sensitivity / parameter analysis.** One parameter effectively swept: the
re-randomisation rate, expressed as "re-randomise every k-th probe". Incremental
case: every 4th vs every 100th probe spans ~6 orders of magnitude in
attack-success probability; every 50th/100th → success "quickly exceeds 90%";
only ~4–25 probes helps (L96–100, Fig. 2.2). Method: analytical curve, not
sampled runs. Reported as probability-vs-rate figure (L94). One empirical
anchor quoted: Shacham's brute-force on PaX ASLR ~216 s on average (L102–103);
ISR re-randomisation every 100 ms at ~14% overhead (L100–101). The extraction
itself uses this as the "sweep-width justification" for the thesis — MTD effect
is "hypersensitive to the shuffle-interval ÷ attacker-action-time ratio, so a
wide sweep on that ratio is mandatory" (L105–108) — but that is the extractor's
inference, not a statement of the paper.

**(d) Convention statements.** None of the "studies typically…" form. The
nearest is the paper's own thesis, paraphrased at L7–8: MTD's benefit is "often
much less significant than one would expect" and conditional on attack class and
re-randomisation rate. No statement about evaluation conventions in the field.

**(e) Relevance to an experiments-chapter design.** Relevant, but only as the
*mechanism* argument for why the shuffle-interval / attacker-action-time ratio
must be swept over a wide range rather than reported at a point (L105–111). It
carries no replication, seeding, or CI convention; it is an analytical paper.

---

## 2. `mtd_stealth_effectiveness.md` (94 lines)

**(a) Papers + citation lines.** Two papers (L25–28):
- `venkatesan2016` — Venkatesan, Albanese, Cybenko, Jajodia, *A MTD Approach to
  Disrupting Stealthy Botnets*, MTD@CCS'16 (L25–26). Pages: Abstract + §1–§2 (L29).
- `sharma2025` — Sharma, *Evaluating MTD Methods Using TTC and Security Risk
  Metrics in IoT*, Electronics 14(11):2205, 2025 (L26–28). Pages: Abstract + §1 +
  "key contributions" (L29–30). NB a fuller `docs/sources/lit_review/sharma2025.md`
  and `.pdf` exist in the repo (see census); this extraction is abstract-level only.

**(b) Evaluation design.**
- Venkatesan: periodically re-places network detectors (centrality-based
  strategies) against a stealthy botnet routing exfil through relay bots;
  "validated in simulation"; a lower-bound detection-probability algorithm is
  given (L38–45). Metric: successful-exfiltration probability / attacker effort
  (L42–45). Network topology, botnet size, replication counts, presentation: not
  in extraction.
- Sharma: attack-path-based MTTC + security-risk metrics on shuffling/diversity
  MTD in an IoT smart-home case study, simulation (L63–68, L77, L92). Metrics:
  mean / min / max TTC (L61). Network setup, replication counts, presentation: not
  in extraction.

**(c) Sensitivity / parameter analysis.** Sharma evaluates "for different
attacker skill levels and shuffling frequencies" (L64–66) — two swept factors:
shuffle frequency and attacker skill. Reported direction: MTTC rises with shuffle
frequency and falls with attacker skill (L66–68). Ranges, step sizes, method
(one-at-a-time vs grid), and whether variance was reported: not in extraction.
Venkatesan: compares centrality strategies (L39, L91–92); no parameter sweep
detail in extraction. The extraction reads the two Sharma axes as "the two sweep
axes for the tuned group" (L66, L72–74) — extractor's mapping, not the paper's
convention claim.

**(d) Convention statements.** None. The extraction's own framing note at
L82–85 ("Both are MTD-effectiveness *metrics* on models/simulations, not logs of
MTD→APT effect") is the extractor's, not a claim about field practice.

**(e) Relevance to an experiments-chapter design.** Relevant as precedent for a
two-factor design (shuffle frequency × attacker skill) with MTTC as response, and
for reporting min/mean/max TTC rather than the mean alone (L61). No replication
or CI conventions carried.

---

## 3. `mtd_scan_disruption.md` (377 lines)

**(a) Papers + citation lines.** Themed bundle, ten papers. Bibliographic
anchor L35–49:
- `carroll2014` — Carroll, Crouse, Fulp, Berenhaut, *Analysis of Network Address
  Shuffling as a MTD*, IEEE ICC 2014 (L35–36). Read: full text (L50).
- `crouse2015` — Crouse, Prosser, Fulp, *Probabilistic Performance Analysis of MT
  and Deception Reconnaissance Defenses*, MTD'15 (L36–38). Full text.
- `anderson2016` — Anderson, Mitchell, Chen, *Parameterizing Moving Target
  Defenses*, IFIP NTMS 2016 (L38–39). Full text.
- `fergusonwalter2021` — Ferguson-Walter, Major, Johnson, Muhleman, *Examining
  the Efficacy of Decoy-based and Psychological Cyber Deception*, USENIX Security
  2021 (Tularosa Study) (L39–42). Read: §6 results only (L51).
- `reti2022` — Reti, Elzer, Fraunholz, Schneider, Schotten, *Evaluating Deception
  and MTD with Network Attack Simulation*, MTD'22 (L42–43). Full text.
- `wang2016_sdn` — Wang, Wu, *MTD Against Network Reconnaissance with SDN*, ISC
  2016 (L43–44). Full text.
- `zhang2023_drl` — Zhang et al., *How to Disturb Network Reconnaissance: a DRL
  MTD Approach*, IEEE TIFS 2023 (L45–46). Value sections only.
- `torquato2022` — Torquato, Maciel, Vieira, *Software Rejuvenation Meets MTD:
  Time-Based VM Migration*, ISSRE 2022 (L46–47). Value sections only.
- `jafarian2015_rhm` — Jafarian, Al-Shaer, Duan, *An Effective Address Mutation
  Approach for Disrupting Reconnaissance*, IEEE TIFS 2015 (L48–49). Value sections.
- Wang 2017 (RDAM) — appears only as a section header "Wang 2017 (RDAM)" (L286);
  no author list / venue in the bibliographic anchor. Citation line: not in
  extraction beyond the header.

**(b) Evaluation design, per paper.**
- Carroll 2014: analytical urn model (n addresses, v vulnerable, k probes) with
  "analysis + empirical" sections (§IV-A/B/E, L57); perfect shuffling caps
  attacker success at 1−e⁻¹ ≈ 0.63 for one vulnerable host and k=n (L59–63);
  benefit collapses as v/n rises (L64–66); cost = legitimate-connection loss vs
  shuffle rate (L66–68). Replication counts, presentation: not in extraction.
- Crouse 2015: probabilistic model with a two-phase attack (recon → wait →
  attack); "Foothold Scenario" (§5.1, Fig. 9, L102); success governed by
  inter-shuffle time ÷ attack-wait-time ratio (L105–110); connection-drop cost
  ~0.04 when inter-shuffle = wait time (L114). Replication: not in extraction.
- Anderson 2016: two cross-validated models (closed-form + Stochastic Petri Net)
  over a 6-phase attack (survey, tool, implant, pivot, damage/exfil, cleanup)
  (L133–135); results in Figs 3–10 (L131). Replication: not in extraction (SPN,
  presumably solved not sampled — not stated).
- Ferguson-Walter 2021: human-subject experiment, 123 professional red-teamers,
  full-day pen-test, 2×2 factorial (decoys Present/Absent × Informed/Uninformed),
  25 Win + 25 Linux real hosts + 25+25 decoys (L164–166). Metrics: files
  exfiltrated (means with per-cell n, e.g. n=13 vs n=6 — L168–169), module
  loads, self-reported exploit successes, real hosts targeted, packet-waste %,
  time-to-first-real-target in minutes (L168–177). Hypothesis testing implied
  ("H2 supported", L179). CI / variance: not in extraction.
- Reti 2022: NASim discrete-event simulator, three rule-based agents (careful /
  standard / aggressive) over scan → service/OS/vuln scan → exploit/privesc →
  wiretapping (L201–205); MTD = address mutation every N steps; all actions cost
  1 step (L229–230). Metrics: win probability, P(compromise all sensitive hosts),
  P(one host) (L209–217). Network sizes 10 vs 50 hosts (L218). Replication
  counts per cell: not in extraction. Presentation: Figs 1–6 (L199).
- Wang 2016: SDN prototype, Tables 1–2 (L236); scan completes ~14 s; decoy
  latency 0.015 s vs real 0.00015 s (L244–245). No dwell; no replication in
  extraction.
- Jafarian 2015: analytical + game-theoretic; metrics deterrence ratio =
  T_RHM/T_static, detectability ratio = C_RHM/C_static (L262–265). Setup /
  replication: not in extraction.
- Wang 2017 RDAM: Mininet/POX simulation, 12,000 internal / 6,000 public hosts,
  Class-B space (L288, L292); miss-rate outcomes 96.2%, 37%, 80% (L292–295), Figs
  5–6 (L288). Replication: not in extraction.
- Zhang 2023 DRL: A2C host mutation; −25% scan hits, +26% / +58.7% scan time
  (L317–320); analysis Eqs 21–24 (L315). Setup / replication: not in extraction.
- Torquato 2022: SPN model of time-based VM migration, RQ1–3 (L337), >40%
  attack-success reduction, availability-vs-security trade-off in the migration
  interval (L342–346). Replication: not in extraction (SPN).

**(c) Sensitivity / parameter analysis.** This is the bundle's substance — every
paper varies a rate/interval and reports a curve, but the extraction records
ranges only for some:
- Carroll: shuffle rate as normalised rate; connection loss "climbs sharply past
  a ~0.85 normalised rate ≈ shuffle every 38 probes" (L67–68); v/n varied (L64–66).
- Crouse: inter-shuffle time vs attack-wait-time ratio (L105–110) — a ratio
  sweep; range not in extraction.
- Anderson: declared values, explicitly recorded as the "precedent for Tier-3
  declare-and-sweep": churn time h ∈ {30, 60, 240} min; attack length c ∈ {8, 24,
  48} h; guidance "months" for nation-state, "hours" for recreational; implants
  i = c/h × o/2 (L138–141). Two emergent cautions: mis-parameterised MTD can make
  the system less secure below a breakeven configuration count (L142–144);
  longer campaigns less likely to succeed under churn (L144–146). Method: model
  evaluation over a small discrete grid (3 × 3 by the values listed; whether full
  factorial: not in extraction).
- Ferguson-Walter: 2×2 factorial design (L164–165); factor levels are the only
  "sweep".
- Reti: mutation interval N ∈ {25, 50, 75, 100} (L206); network size 10 vs 50
  hosts (L218); agent type as a third factor (L202–204). Reported as win
  probability vs interval per agent (L209–214).
- Wang 2017: r = scan-rate ÷ mutation-rate; miss probability rises as r falls;
  no benefit when r ≥ k (L296–299). Range of r: not in extraction.
- Torquato: migration interval swept; trade-off reported (L344–346). Range: not
  in extraction.
- Zhang DRL, Jafarian, Wang 2016: no sweep detail in extraction.

**(d) Convention statements.** No explicit "studies typically…" sentence. Two
extractor-level generalisations that function as conventions in this repo:
- L138–141: Anderson's declared values are "the *precedent* for Tier-3
  declare-and-sweep" and L148–150 "a *precedent* for declaring a tactic dwell +
  sweeping it, not a value to transplant".
- L360–364: "Every reset verdict here is **modelled/declared**, never a logged
  real-world MTD→APT effect … The consistent *shape* across analytical
  (Carroll/Crouse), SPN (Anderson), DES (Reti), and human-subject
  (Ferguson-Walter) evidence is the argument; the *magnitude* is swept."
Both are the extractor's synthesis, not quotations from the papers. Paper-side
quoted conventions: Carroll's cited DARPA/DYNAT figure "an attacker can be
expected to spend upwards of 45% of their time performing reconnaissance" and
Rowe & Goh "attackers can wait up to a day before acting on recon" (L68–71);
Wang 2016's ">70% of network scans are connected with attack activities"
(L242–243); Zhang's Panjwani "up to 70% of cyber attacks are preceded by
scanning" (L321–322). These are attacker-behaviour statistics, not evaluation
conventions.

**(e) Relevance to an experiments-chapter design.** Highly relevant — the
richest source in the set for *design shape*: (i) a single-factor interval sweep
with a small discrete level set (Reti N ∈ {25,50,75,100}; Anderson h ∈
{30,60,240} min) crossed with attacker type and network size; (ii) a 2×2
factorial with per-cell n and means (Ferguson-Walter); (iii) the ratio
(interval ÷ attacker action time) as the natural x-axis (Crouse, Wang 2017,
Anderson). Absent from every row: replication counts per cell, seeds, CIs,
warm-up — none are in the extraction.

---

## 4. `timed_attack_models.md` (204 lines)

**(a) Papers + citation lines.** Bundle of thirteen formal attacker-timing
models (L30–47):
- `katsikeas2020_corelang` — coreLang, GraMSec 2020 (L30).
- `madan2004` — Madan, Goseva-Popstojanova, Vaidyanathan, Trivedi, *Modeling &
  quantifying security attributes of intrusion-tolerant systems*, Performance
  Evaluation 56, 2004 (L31–33).
- `johnson2018_mal` — Johnson, Lagerström, Ekstedt, *A Meta Language for Threat
  Modeling and Attack Simulations*, ARES'18 (L33–34).
- `holm2015_p2cysemol` — Holm et al., *P2CySeMoL*, IEEE TDSC 12(6), 2015 (L35).
- `johnson2016_pwnpr3d` — Johnson, Vernotte, Ekstedt, Lagerström, *pwnPr3d*,
  ARES'16 (L36–37).
- `widel2023_mal` — Wideł et al., *The MAL – A Formal Description*, Computers &
  Security 130, 2023 (L37–38).
- `katsikeas2022_vehiclelang` — VehicleLang, Computers & Security 117, 2022 (L38–39).
- `almasizadeh2013` — Almasizadeh, Azgomi, *A stochastic model of attack
  process*, Computer Networks 57(10), 2013 (L39–40).
- `orojloo2018` — Orojloo, Azgomi, *Security of CPS using SPN*, IET
  Cyber-Physical Systems 3(2), 2018 (L41–42).
- `zhou2019` — Zhou, Reniers, Zhang, *Petri-net based attack time analysis*,
  Comp. & Chem. Eng. 130, 2019 (L42–43).
- `wu2021` — Wu et al., *Stochastic Evolutionary Game SPN*, Security & Comm.
  Networks, 2021 (L43–44).
- `liu2019` — Liu, Xing, Zhou, *Probabilistic modeling of sequential
  cyber-attacks*, Engineering Reports 1(4), 2019 (L44–46).
- `tripathi2022` — Tripathi et al., *GSPN NPP*, Annals of Nuclear Energy 168,
  2022 (L46–47).
- `lalropuia2019` — NOT extracted; wrong file downloaded (L54–60).
Pages read: mostly Abstracts and single sections (L48–52) — this bundle is
abstract-level for most rows.

**(b) Evaluation design.** All are analytical / solved models, not sampled
simulation studies (as far as the extraction records):
- Madan 2004: semi-Markov process for SITAR intrusion-tolerant system; security
  failure states absorbing; MTTSF computed; "analysis … depends only on the mean
  sojourn time and is independent of the actual sojourn time distributions"
  (L101–107). No network/replication detail (analytical).
- MAL family: per-attack-step TTC distribution declared, aggregate TTC computed
  over an auto-generated attack graph by simulation ("a simulation yields a
  probabilistic estimate of the time to compromise each attack step", L130–132).
  Number of simulation samples: not in extraction. P2CySeMoL's per-step
  provenance: "literature, domain experts, surveys, observations, experiments
  and case studies" (L133–136).
- Almasizadeh, Orojloo, Zhou, Wu, Liu, Tripathi: semi-Markov / SPN / TCPN /
  CTMC / GSPN models solved for MTTSF / MTTF / MTTR / mean-time-to-disrupt /
  attack success rate / availability (L160–177). Orojloo declares an
  "input-parameter table" of mean holding time per state + transition
  probabilities (L164–166). Replication counts, presentation: not in extraction.

**(c) Sensitivity / parameter analysis.** The extraction's headline claim is
that these models' "shared move is exactly ours: assign a probability
distribution / sojourn time to each attack step or state, from expert/literature
elicitation, then run sensitivity analysis" (L8–10) and that the cluster
"executes the declare-per-state-time → solve-for-aggregate → sweep move" (L159).
Concrete sweeps recorded:
- Zhou 2019: "sweeps the surveillance/inspection interval from 5 to 100
  minutes and reads off security-failure probability" (L167–170). Step size,
  method: not in extraction.
- Orojloo 2018: restoration transition rate 1/Tr as the reset rate (L166) —
  whether swept: not stated.
- Madan 2004: "depends only on the mean sojourn time" for steady state
  (L105–107) — a distributional-insensitivity result rather than a sweep.
For every other row (MAL family, Almasizadeh, Wu, Liu, Tripathi): sensitivity
method, parameters, ranges: not in extraction. NB the L8–10 "then run
sensitivity analysis" is a bundle-level generalisation by the extractor; only
Zhou is documented performing one.

**(d) Convention statements.** The strongest convention claims in the whole
set, but they are the extractor's:
- L8–12: "Their shared move is exactly ours: assign a probability distribution
  / sojourn time to each attack step or state, from expert/literature
  elicitation, then run sensitivity analysis. They are the field norm the
  operational-validation note claims."
- L24–26: "declare-and-sweep is the field norm; Step-F justification that a
  declared per-state dwell + sweep is a recognised, not ad-hoc, construction".
- L143: "declared per-technique/step TTC is the field norm".
- L195–198: "Every model here **declares** its per-step/per-state timing
  (expert/literature/CVSS-elicited) — none measures per-ATT&CK-tactic dwell."
Paper-side: P2CySeMoL "flagging that expert estimates are valid only for their
time/scope/competence" (L136) — a caveat on elicited parameters.

**(e) Relevance to an experiments-chapter design.** Relevant as the
*methodological lineage* for declared-parameter models with an interval sweep
(Zhou 5–100 min) and for the "mean is what matters" licence (Madan). It carries
no simulation-replication, seed, or CI conventions; the models are mostly solved
analytically. The "field norm" phrasing at L8–12 and L24 is an extractor
synthesis over abstracts and should be cited as the repo's reading, not as a
literature claim, until a primary is checked.

---

## 5. `rl_security_environments.md` (74 lines)

**(a) Sources + citation lines.** Survey-level stub, no peer-reviewed paper
extracted (L3–4, L22–25). Citation keys `cyberbattlesim`, `nasim`, `cyborg`
(L12). Sources: CyberBattleSim GitHub (L14); MIT MEng thesis "Simulating Network
Lateral Movements through the CyberBattleSim Web Platform",
dspace.mit.edu/handle/1721.1/143191 (L14–16); "Evaluation of RL for Autonomous
Penetration Testing (A3C/Q-learning/DQN)", arXiv:2407.15656 (L17–18); Kim-Hammar
*awesome-rl-for-cybersecurity* GitHub (L19). Authors / year for the arXiv paper:
not in extraction.

**(b) Evaluation design.** Only environment structure is recorded:
CyberBattleSim = directed graph of nodes with OS/services/vulns/firewall rules,
RL attacker over a typed action space (local exploit, remote exploit,
credential-based lateral movement) under partial observability, reward
asymmetric toward mission-critical nodes (L31–37); NASim = declarative action
model with prerequisites, cost, success probability (L37–39); CybORG =
defender-side (L39–40). Network sizes, scenarios, replication counts, metrics,
presentation: not in extraction.

**(c) Sensitivity / parameter analysis.** Not in extraction.

**(d) Convention statements.** L49–51: "The mission-critical-node reward
asymmetry corroborates that *objective-weighted target selection* is a standard,
defensible mechanism" — extractor's verdict, survey-level. L66–68: CyberBattleSim's
"noted advance over earlier simulators (incl. NASim) is explicit credential
handling" — survey-level. No evaluation-convention statements.

**(e) Relevance to an experiments-chapter design.** Not relevant to
evaluation design; it is a modelling-precedent note (action-space framing for
controller candidate C3, L41–58). The one usable design point is the note that
"the substrate samples under a seeded stream" and that RL training "would break
SIM-05 determinism" (L55–58) — a repo constraint, not a literature one.

---

## 6. `mcqueen2006.md` (267 lines)

**(a) Paper + citation line.** McQueen, Boyer, Flynn, Beitel, "Time-to-Compromise
Model for Cyber Risk Reduction Estimation", in *Quality of Protection* (QoP
Workshop @ ESORICS 2005), Springer, 2006, pp. 49–64; INL preprint
INL/CON-05-00649, OSTI 911165 (L3–6). DOI 10.1007/978-0-387-36584-8_5; preprint
https://www.osti.gov/biblio/911165 (L30–31). Read: full preprint text, 17 pp
(L32–33). NB: this one IS in the repo as source markdown + PDF (L7–8,
`docs/sources/tactic_profiles/step_c/`, gitignored) — the extraction's "[fetched]"
marks are against full text, so this block is less extraction-only than the
others, though the survey still only reads the extraction.

**(b) Evaluation design.** Analytical model + one worked case study: TTC as a
three-process random variable (P1 known vuln + ready exploit; P2 known vuln, no
exploit; P3 new-vuln discovery) composed by Eq. 6 (L41–57). Case study on the
CS60 SCADA testbed, dominant-path component APPS1, expected TTC in days for four
skill levels under baseline / enhanced / hypothetical-zero-vulns configurations:
55.5/13.2/6.5/2.9; 79.1/15.2/7.6/3.8; 193.4/92.0/45.9/21.0 (L136–139). Metric:
expected TTC only — "For now, the analysis only uses the expected value of the
time-to-compromise" (L211–214); hypothesised beta/gamma/exponential PDFs are
never used (L59–62, L212–213). Replication: none (deterministic expectation).
Presentation: Fig. 8, Fig. 9 tables (L134, L144). Explicit disclaimer: "These
estimates of time-to-compromise have not been validated but simply show how the
model may be applied to a real system" (L145–146).

**(c) Sensitivity / parameter analysis.** No sensitivity analysis performed;
§7 names "validation experiments and **sensitivity analysis** … as future work"
(L116–117). Parameter variation present is the skill gradient (four levels via
m ∈ {50,150,250,450} and AM/V ∈ {0.15,0.30,0.55,1.00}, L93–96, L106–108) and
three vulnerability configurations (19 / 11 / 0 root-access vulns, L148–149).
The paper's own reading: "for skilled attackers the time-to-compromise is not a
strong function of the number of vulnerabilities" (L143–144); 86% total vuln cut
→ only 13–30% TTC rise on the dominant path (L140–142).

**(d) Convention statements.** The declare-and-justify register, quoted:
- L85–90 (§1): "The estimation of time-to-compromise is particularly difficult
  because of the lack of reliable data. We recognize that some of the
  assumptions associated with our model have not been validated but we have
  attempted to provide justification with real data when data is available. We
  have used expert elicitation or have made simple assumptions when data is
  unavailable."
- L99–100: "Somewhat arbitrarily, we decided to use 8 hours (one working day)
  as the mean time for a successful attack in Process 1".
- L112–117 (§6): self-declared drawbacks — m-as-skill-proxy not validated;
  uniform-exploit assumption "is incorrect"; P1/P2 PDFs not validated.
- L238–245: extractor's "Emergent idea — the sweep discipline is inherited, not
  invented … twenty years on, the field (Bland 2020, MAL, TTC_ICS) still runs
  exactly this pattern" — explicitly marked "our synthesis; the paper doesn't
  make the historical claim" (L247–248).
- L119–121: extractor: "Tier-3 discipline: declared + justified + swept is the
  lineage norm from the root".

**(e) Relevance to an experiments-chapter design.** Relevant as the founding
precedent for (i) reporting expected values only and saying so, (ii) declaring
parameters with provenance per parameter, (iii) admitting un-validated
assumptions in the text, and (iv) naming sensitivity analysis as the required
follow-up. It supplies no replication / seed / CI conventions and performs no
sensitivity analysis itself.

---

## 7. `persistence_reset_models.md` (129 lines)

**(a) Papers + citation lines.** Three (L28–33):
- `vandijk2013_flipit` — van Dijk, Juels, Oprea, Rivest, *FlipIt: The Game of
  "Stealthy Takeover"*, J. Cryptology 26(4), 2013 (L28–29). Read: Abstract + §1
  + §4 (L34).
- `huang2006_scit` — Huang, Arsenault, Sood, *Incorruptible System
  Self-Cleansing for Intrusion Tolerance* (SCIT), IEEE IPCCC 2006 (L30–31). Read
  §1–§5, OCR-garbled, figures `[parse-uncertain]` (L34–35, L79–80).
- `sun2025_flipit` — Sun, Fei, Zhu, Guo, *MARL for MTD Temporal Decision-Making
  (Stackelberg-FlipIt)*, CMC 84(2), 2025 (L31–33). Read §1–§4 (L35–36).

**(b) Evaluation design.**
- FlipIt: game-theoretic / analytical; benefit = fraction of time controlling
  the resource − average move cost; results are equilibrium theorems (higher
  move cost → benefit 0; periodic-with-random-phase dominates renewal
  strategies of the same rate) (L44–55). No simulation, replication, or network
  setup in extraction.
- SCIT: system design; cleansing-cycle length = maximum attacker-hold window
  (L73–77). Exact cycle figures `[parse-uncertain]` (L79–80). No evaluation
  detail in extraction.
- Sun 2025: Stackelberg + multi-agent RL (WoLF-PHC) learning move timing;
  "validated on IP-address dynamic hopping against scanning" (L98–104). Metrics,
  network, replication: not in extraction.

**(c) Sensitivity / parameter analysis.** No sweep recorded for any of the
three. The extractor's reading is that all three "price the reset-rate ÷
compromise-rate ratio" (L9–11) and that "the reset is partial and rate-dependent
… The magnitude is swept" (L118–121) — the sweep is the thesis's, not the
papers'. Sun states the trade-off qualitatively: "insufficiently reactive MTD
intervals grant attackers extended time windows …" vs overly aggressive
intervals cause instability/overhead (L100–103). Ranges: not in extraction.

**(d) Convention statements.** None about evaluation practice. L104–105 (Sun):
"when to move" (the reset interval) is "*the* decision variable and is
adversary-conditioned" — extractor paraphrase of the paper's framing.

**(e) Relevance to an experiments-chapter design.** Marginal. Supplies the
argument that the reset interval is the natural swept factor and that a
periodic-with-random-phase schedule is the theoretically preferred defender
strategy (L51–53) — relevant if the experiments chapter must justify a periodic
MTD trigger. No replication / reporting conventions.

---

## 8. `mttc_lineage.md` (121 lines)

**(a) Papers + citation lines.** Three (L29–33):
- `leversage2008` — Leversage & Byres, *Estimating a System's Mean
  Time-to-Compromise*, IEEE S&P 6(1), 2008 (L29–30). Read: §"Process 1",
  §"skills indicator" (L34).
- `zieger2018` — Zieger, Freiling, Kossakowski, *The β-Time-to-Compromise
  Metric*, IEEE IMF 2018 (L30–31). Read: Abstract + §I–IV (L34–35).
- `maleki2016` — Maleki, Valizadeh, Koch, Bestavros, van Dijk, *Markov Modeling
  of MTD Games*, MTD'16 (L31–33). Read: Abstract + §1 (L35).

**(b) Evaluation design.**
- Leversage 2008: McQueen-lineage MTTC; Process-1 mean t₁ = 1 day; continuous
  skills indicator ∈ [0,1] scaling readily-available exploits (m = 450) (L44–50).
  System / case study / replication: not in extraction.
- Zieger 2018: continuous TTC with CVSS vectors and β-distributed skill;
  "validated on a national-CERT vulnerability database" (L68–72). Validation
  method, sample size, metric: not in extraction.
- Maleki 2016: Markov framework; theorems relating adversary success
  probability to time/cost spent; "security capacity" measure; applied to
  IP-hopping and target hiding (L93–99). Numerics: not in extraction (L120–121
  lists "IP-hopping numerics" as out of scope).

**(c) Sensitivity / parameter analysis.** No sweep recorded. Leversage's
continuous skill indicator is read by the extractor as "the skill model
justifies a swept range" (L59) and Zieger's β-skill as "supports a distribution
over the anchor, not a point" (L79–80) — inferences, not paper-reported sweeps.
Maleki: success is a rising function of time-under-MTD (L94–96, L102–103); no
parameter ranges in extraction.

**(d) Convention statements.**
- L72–75 (Zieger, paraphrased): TTC "has evolved into one of the most successful
  cybersecurity metrics in practice" — the extractor reads this as "declaring a
  per-state compromise time and refining it with CTI is the mainstream method".
- L17–18: TTC-lineage per-state declared dwell is "the field's dominant
  declare-a-time precedent" — extractor.
- L23–24: "the method note's 'declare-and-sweep is the field norm' (TTC is the
  exemplar)" — extractor, pointing at the repo's own method note.
- L83–84: "consistent with the survey's gap finding that empirical timing exists
  only at CVE granularity" — extractor.

**(e) Relevance to an experiments-chapter design.** Marginal for design;
relevant for justifying a skill axis as a continuous or distributed factor
(Leversage [0,1] indicator; Zieger β-distribution) rather than discrete levels.
No replication / reporting conventions.

---

## 9. `syed2025.md` (129 lines)

**(a) Paper + citation line.** Syed, Nour, Pourzandi, Assi, Debbabi,
"Comprehensive Advanced Persistent Threats Dataset", *IEEE Networking Letters*
7(2):150–154, June 2025 (L3–5). DOI 10.1109/LNET.2025.3551989; dataset
https://github.com/AbSamad99/APTsDataset (L29–30). Read: full text, 4 pp (L31).
Source md + PDF exist in the repo (L6–8, gitignored).

**(b) Evaluation design.** Not an MTD evaluation; a dataset paper. Testbed:
Caldera attack box + Windows/Linux target VMs with Filebeat/Winlogbeat + ELK
monitoring box (L39–40). 23 campaigns across 12 APT groups (listed L41–44),
11–20 techniques per campaign, 83 techniques, up to 290 abilities across 14
tactics (L44–46). Adversary profiles hand-built from CTI (L46–48). Per campaign
shared: profile, abilities, ELK telemetry, technique sequence (L48–50).
Attacker model: scripted Caldera abilities executed "sequentially at machine
speed" (L66–67). Replication (campaigns re-run?): not in extraction. Metrics:
none (dataset). Presentation: Table II, Fig. 4 (L37, L103).

**(c) Sensitivity / parameter analysis.** Not in extraction (none applicable).

**(d) Convention statements.** L46–48 (quoted §IV-A): "we were not able to
find playbooks that describe the attack sequences for APTs, we referred to
multiple CTI sources and built attack paths based on them" — a statement that
the sequence-from-CTI construction is the available method. L66–74: extractor's
verdict — timestamps measure testbed execution latency, not adversary dwell;
"no pacing, jitter beyond Caldera defaults, or literature-informed tempo is
claimed anywhere in the paper".

**(e) Relevance to an experiments-chapter design.** Not relevant to evaluation
design. Relevant only as the negative-evidence citation that emulation corpora
carry no adversary tempo (L58–74), which the chapter may need when justifying
declared timing.

---

## 10. `ling2023.md` (302 lines)

**(a) Paper + citation line.** Rencelj Ling & Ekstedt, "Estimating
Time-To-Compromise for Industrial Control System Attack Techniques Through
Vulnerability Data", *SN Computer Science* 4:318, 2023, open access (L3–5). DOI
10.1007/s42979-023-01750-z (L30). Read: full text, 11 pp (L31). Source md + PDF
in repo (L6–7, gitignored).

**(b) Evaluation design.** Analytical TTC_ICS model (McQueen lineage, Eqs 1–4,
L40–57) applied to an ICS vulnerability dataset (k = 2740, Thomas & Chothia
2020, L77–78). Outputs: TTC in days for two assets × three vulnerability
categories × four skill levels, Table 7 (L112–122). Attacker model: skill
levels novice/beginner/intermediate/expert, with per-skill exploit development
times t2 = 37/27/16/6 days from the RAND range (L79–82) and per-skill
exploitable fractions f = 0.05/0.24/0.50/1 from CVSS exploitability (L88–91).
Replication: none (deterministic expectation). Validation: none — "we are
unable to compare it directly to other existing TTC approaches", expert
interview validation is future work (L150–151). Presentation: Table 7,
Discussion (L110). Sample-size caveat: 148 HMI vulns vs 32 protection-system
(L146–148).

**(c) Sensitivity / parameter analysis.** No formal sensitivity analysis in
extraction. One ad-hoc correction that functions as a single-parameter
perturbation: the MTBV = 0 artefact row corrected with the category-average
MTBV of 14 days → 258/44/17/6 instead of 37/27/16/6 (L124–125). The skill
dimension is the only varied factor; the extractor observes that "the
four-orders-of-magnitude spread lives entirely in the skill dimension, not the
technique dimension" (L169–171) and the expert column is a constant 6 days
(L154–155, quoted). Ranges of other parameters: not swept.

**(d) Convention statements.**
- L82–84 (quoted): "Even though the report is not ICS specific, we assume that
  the time that it takes to develop an exploit is the same for the ICS domain
  as for any other domain." — a declared cross-domain assumption.
- L97–99 (quoted): "In reality the value shows how often a vulnerability is
  reported … but we use it as an indication of how often vulnerabilities are
  found." — proxy admitted in text.
- L101–104: extractor — "even the empirical frontier rests on declared
  skill-splits and proxies; cite when defending Tier-3 declare-and-sweep as
  continuous with, not weaker than, the field's 'empirical' practice."
- L269–271: Xiong, Hacks & Lagerström 2021 (CSIMQ 26) characterised as
  assigning TTC distributions "by systematic literature review with per-source
  credibility ratings", whose authors "acknowledge that the result is
  qualitative rather than quantitative" — second-hand via ling2023, CSIMQ paper
  unread (L277–279).
- L243–246: ethical-hacker survey (Bromiley 2022, SANS/Bishop Fox): majority
  break in within 1–5 h of finding an exposure and collect data within 1–5 h of
  access — second-hand, flagged [search].

**(e) Relevance to an experiments-chapter design.** Relevant for (i) the
skill-level factor as a four-level discrete design and the finding that skill
dominates technique identity at expert level (L168–174), and (ii) the
declared-parameter provenance register. Not relevant for replication / CI /
sweep method — none in extraction.

---

## 11. `xiong2021.md` (214 lines)

**(a) Paper + citation line.** Xiong, Legrand, Åberg, Lagerström, "Cyber
security threat modeling based on the MITRE Enterprise ATT&CK Matrix",
*Software and Systems Modeling* 21:157–177, 2022 (online 18 June 2021; open
access) (L3–6). DOI 10.1007/s10270-021-00898-7 (L28). Read: surviving md text in
full (L29, L205–206). Source md + PDF in repo (L7–8, gitignored). Disambiguation:
NOT the CSIMQ companion Xiong, Hacks & Lagerström 2021, CSIMQ 26:55–77 (L31–36),
which is fetched but only note-level read (L186–200).

**(b) Evaluation design.** MAL-based enterpriseLang; per-step local TTC
sampled from an assigned distribution, global TTC = shortest path from entry,
computed by modified SSSP "wrapped in Monte Carlo (sampled graphs; the resulting
global-TTC set approximates the distribution)" (L79–84). Performance: "1000
sampled graphs at ~half a million nodes in under three minutes" (L85–86) — the
only sample-count number in the twelve extractions. Attacker model: rational,
shortest path (L86–87). Case studies: Ukraine simulation (§6.1), Cayman
National Bank (§6.2) (L42, L165). Headline: published enterpriseLang ships
*untimed* — "the lines are of equal width owing to the lack of probability
distributions that can be assigned to attack steps" (L52–55, quoted §6.1);
assigning distributions deferred to future work (L57–59). Metrics, presentation
beyond figure width: not in extraction. §7 Discussion lost in parse (L201–205).

**(c) Sensitivity / parameter analysis.** Not in extraction (no distributions
assigned, so none possible in the published paper). CSIMQ companion: assigns
distributions by "systematic literature review with credibility assessment"
and converts qualitative information into distributions, e.g.
`Bernoulli(0.712)·Exponential(1)` for a step (L188–198); no sensitivity method
recorded.

**(d) Convention statements.**
- L104–107: extractor — "direct formal precedent that 'time to objective = sum
  of per-state times along a path' is standard attack-simulation semantics".
- L192–193 (CSIMQ, quoted fragment): prior default was that "we often rely on
  security experts to model them" — a stated field convention for TTC
  parameter sourcing, with the SLR method framed as an improvement.
- L83–84: Monte Carlo over sampled graphs is how MAL approximates the global
  TTC distribution — method convention of the MAL family.

**(e) Relevance to an experiments-chapter design.** Relevant as (i) the one
extraction that records a Monte Carlo sample count (1000 graphs) and the
additive-path TTC semantics, and (ii) the CSIMQ statement that expert
declaration was the prevailing parameter source. No replication-per-cell, CI,
or sweep conventions.

---

## 12. `selmanaj2024.md` (239 lines)

**(a) Source + citation line.** Selmanaj, *Adversary Emulation with MITRE
ATT&CK: Bridging the Gap Between the Red and Blue Teams*, O'Reilly Media, April
2024, 1st ed., ISBN 978-1-098-14376-3 (L3–4, L30). Textbook, not a paper. Read:
Ch. 2, Ch. 4, Ch. 5 opener (L31–33). Source md + PDF in repo (L5–6, gitignored).

**(b) Evaluation design.** None — a practitioner textbook (L192). Records the
dwell-cadence taxonomy (smash-and-grab vs slow-and-deliberate, L42–49), dwell
time defined as MTTD + MTTR in days (L49–52), the re-reported Mandiant global
median dwell 416 days (2011) → 21 days (2021) (L70–74), and one behavioural
paragraph per tactic (L93–189). Network / attacker model / replication /
metrics: not in extraction (not applicable).

**(c) Sensitivity / parameter analysis.** Not in extraction.

**(d) Convention statements.**
- L10–12: extractor — "the precedent survey's adversary-emulation-frameworks
  section noted no emulation resource attaches per-phase dwell; this is the
  canonical emulation *textbook* and it confirms that — behaviour and cadence,
  no per-tactic time."
- L49–52: dwell time = MTTD + MTTR, "the longer the dwell time, the more
  opportunity the adversary has to cause harm" — practitioner metric
  convention.
- L83–85: extractor — "keep only as evidence the dwell metric is standard
  practitioner vocabulary".

**(e) Relevance to an experiments-chapter design.** Not relevant to
evaluation design. Relevant only for vocabulary (dwell time as the practitioner
outcome measure) and for the cadence dichotomy if attacker tempo classes are a
design factor.

---

## Cross-extraction summary (extraction-only)

What the twelve extractions collectively carry on evaluation conventions:

| Convention element | Carried by | Not carried by |
|---|---|---|
| Interval / rate sweep as the primary factor | evans2011 (probe-rate, L96–100); mtd_scan_disruption — Reti N∈{25,50,75,100} L206, Anderson h∈{30,60,240}min L139, Crouse ratio L105–110, Wang2017 r L296–299, Torquato L344–346; timed_attack_models — Zhou 5–100 min L167–170; mtd_stealth — Sharma shuffle freq L64–66 | mcqueen2006 (sweep named as future work L116–117), ling2023, xiong2021, syed2025, selmanaj2024, rl_security_environments, persistence_reset_models, mttc_lineage |
| Attacker skill / type as second factor | mtd_stealth Sharma L64–66; mtd_scan_disruption Reti agent types L202–204; mcqueen2006 four skills L93–96; ling2023 four skills L44; mttc_lineage Leversage continuous [0,1] L47–48, Zieger β L69–70 | — |
| Network size as factor | mtd_scan_disruption Reti 10 vs 50 hosts L218; Wang2017 12,000/6,000 hosts L292; Ferguson-Walter 50 real + 50 decoy L165–166 | all others |
| Factorial design stated | mtd_scan_disruption Ferguson-Walter 2×2 L164–165 | all others |
| Per-cell n / replication count | Ferguson-Walter n=13 vs n=6 participants L168–169; xiong2021 1000 sampled graphs L85 | every other row: not in extraction |
| Seeds, CIs, variance, warm-up, steady state | none (Madan "steady-state" L107 is a solution regime, not a warm-up convention) | all |
| Expected-value-only reporting, stated | mcqueen2006 L211–214 | — |
| Min/mean/max reporting | mtd_stealth Sharma L61 | — |
| Sensitivity analysis named as required follow-up | mcqueen2006 §7 L116–117 | — |
| Parameter provenance register (per parameter source + admitted assumption) | mcqueen2006 L85–117; ling2023 L74–99; timed_attack_models P2CySeMoL L133–136 | — |
| "Declare-and-sweep is the field norm" | extractor synthesis only: timed_attack_models L8–12, L24, L143; mttc_lineage L23–24; mcqueen2006 L119–121, L238–245; mtd_scan_disruption L138–141, L360–364 | no paper-side statement of this form in any extraction |


---

## grep census

Terms: sensitivity, Sobol, Saltelli, one-at-a-time, OAT, Morris, factorial,
confidence interval, replication, Monte Carlo, warm-up, steady state, seeds,
variance. Tree: `docs/sources/` (extractions/, lit_review/, tactic_profiles/,
gopen_swan). Raw hit count 307 lines across ~95 files; listed below: 60 hits,
one per file where possible, strongest methodological hit chosen. Zero hits
anywhere for: Sobol, Saltelli, one-at-a-time, OAT, Morris (as a method —
"Morris worm" and "Morris-King" author hits excluded). "Replication" hits in
alavizadeh2022 / hong2018 / masud2025 / unit42 are VM/service replication (the
MTD technique), not experimental replication — excluded. "Warm-up" has one hit,
service warm-up in a testbed (ferraz2024 L307), not simulation warm-up.

**Caveat discovered by the census:** `docs/sources/tactic_profiles/step_c/` and
`step_d/` hold the *source markdowns* (gitignored, but present locally) of many
papers the extractions above paraphrase — mcqueen2006, ling2023, xiong2021,
selmanaj2024, syed2025, Reti 2022, Anderson 2016, Torquato 2022, Madan 2004,
Orojloo 2018, Evans 2011, Jafarian 2015, etc. The blocks above were written
extraction-only per the brief and were NOT verified against those files; the
census hits below from `tactic_profiles/` are the first direct look at them.

### extractions/

1. `docs/sources/extractions/timed_attack_models.md:10` — "assign a probability distribution / sojourn time to each attack step or state, from expert/literature elicitation, then run sensitivity analysis. They are the field norm the operational-validation note claims." [extractor synthesis]
2. `docs/sources/extractions/mcqueen2006.md:116` — "§7: validation experiments and **sensitivity analysis** named as future work."
3. `docs/sources/extractions/zhang2023.md:105` — "Z-TIM-02 | Each MTD technique has its own execution time (mean, std). Values are picked 'within a reasonable range based on existing empirical data' + sensitivity analysis | §4.3.4"
4. `docs/sources/extractions/cho2020.md:108` — "| Simulation | Better flexibility in attack/system modeling than analytical models; easy parameterization for sensitivity analysis | Limitations due to inherent uncertainty toward real-world applications |"
5. `docs/sources/extractions/cho2020.md:52` — "its scoped contribution is sensitivity-analysis around the rational-actor and learning-capability asymmetries" [extractor, thesis framing]
6. `docs/sources/extractions/xiong2021.md:83` — "shortest-path algorithm wrapped in Monte Carlo (sampled graphs; the resulting global-TTC set approximates the distribution)"
7. `docs/sources/extractions/mendonca2023.md:123` — "estimated rows — *declared notional, swept for sensitivity*, never presented as" [extractor]
8. `docs/sources/extractions/tay2024.md:98` — "T-EVAL-05 | Detection-sensitivity cutoff at 0.7: between 0.7–1.0 sensitivity, performance improves monotonically with detection; below 0.7, performance becomes uncorrelated" (IDS sensitivity, a swept parameter, not SA method)
9. `docs/sources/extractions/evans2011_mtd_effectiveness.md:117` — "the transferable finding is the attack-class conditionality and the rate-sensitivity"
10. `docs/sources/extractions/outkin2023.md:35` — "takes a *fixed* ATT&CK-derived attack graph … and a *fixed* attacker, and varies the defender" (design shape: one factor varied)
11. `docs/sources/extractions/worm_propagation_models.md:61` — "steady state 200k–300k, peak 600k over 7 months" (Mirai population, not a simulation convention)

### lit_review/

12. `docs/sources/lit_review/1_1_cho2020toward.md:698` — "Due to the flexibility and experimental capability to conduct sensitivity analysis by varying the values of key design parameters, it allows us to easily obtain meaningful insights before performing the implementation in a real system." **[convention statement, survey paper]**
13. `docs/sources/lit_review/zhang2023.md:354` — "[Zhang et al.] set the time duration of each MTD technique within a reasonable range based on existing empirical data and conducts sensitivity analysis to determine the appropriate value to perform the evaluation." **[the substrate's own paper]**
14. `docs/sources/lit_review/zhang2023.md:410` — "The parameter µ is the historical average elapsed time, which can be determined via empirical study and sensitivity analysis."
15. `docs/sources/lit_review/sharma2025.md:579` — "This sharp decline highlights the sensitivity of MTD performance to shuffling frequency, emphasizing the necessity of frequent shuffling" (effectiveness drops from ~90% to ~25–35% when shuffle interval goes 1 → 2 days, L576–578)
16. `docs/sources/lit_review/chobenasher2018.md:1114` — "(3) validate the proposed model based on various scenarios through comprehensive sensitivity analysis." (future work)
17. `docs/sources/lit_review/4_outkin2023defender.md:479` — "## 5.1.2 Sensitivity Analysis" (section heading); L45: "calculating the sensitivity of [attack metrics] to defender resource allocation"; L612: "convergence time to steady state may be long … we calculated the 'time-to-success' distribution"
18. `docs/sources/lit_review/manadhatawing2011tse.md:561` — "In our parameter sensitivity analysis, we studied the …" (attack-surface parameter sensitivity; also `manadhatawing2011.md:879` "numeric value assignment using parameter sensitivity analysis [20]")
19. `docs/sources/lit_review/tay2024.md:49` — "Conducted experiments to evaluate the impact of key hyperparameters such as gamma, epsilon and train start … Additional experiments were performed to assess the impact of IDS sensitivity on model performance"
20. `docs/sources/lit_review/tay2024.md:316` — "varying epsilon and epsilon decay had a greater impact on the individual metrics as the variance was higher compared to gamma."
21. `docs/sources/lit_review/2_4_buechel2025sok.md:361` — "has feasible dimensions allowing for reasonable reproducibility" (LLM reproducibility, tangential)
22. `docs/sources/lit_review/2_4_ferraz2024procedural.md:372` — "Another implication concerns environmental sensitivity. Real intrusions reflect the organization's topology…" (not SA)
23. `docs/sources/lit_review/1_1_cho2020toward.md:833` — "Zhang et al. [177] aimed to identify an optimal interval of VM migration" (interval as optimised parameter)
24. `docs/sources/lit_review/3_2_kim2026mtdid.md:586` — ref [32] Ben-Asher, Morris-King, Thompson, Glodek, "Attacker skill defender strategies and the effectiveness of migration-based MTD", ICCWS 2016 (cited in three lit_review files: cho2020 L945, tay2024 L424, kim2026 L586 — a skill × defender-strategy MTD study not extracted anywhere in the repo)
25. `docs/sources/lit_review/1_3_masud2025vulnerability.md:66` — "as MTD techniques have grown, assessing their combined efficacy has become a difficult task (Alavizadeh et al., 2020)"

### tactic_profiles/ (source markdowns, gitignored, present locally)

26. `docs/sources/tactic_profiles/step_d/15_impact/TSP_CMC_71705.md:213` — "Each experimental configuration was repeated 100 times under randomized user behavior and threat injections. For each metric (Accuracy, MTTC, Encryption Success Rate), we report the mean and standard deviation. In addition, 95% confidence intervals were calculated to assess the statistical reliability of the results. Where applicable, paired t-tests were conducted between the proposed framework and baseline models" **[the fullest replication+CI+test statement in the tree; MTD/MTTC paper, CMC 2025, also filed at 0_cross_tactic_timed_models/]**
27. `docs/sources/tactic_profiles/step_d/15_impact/TSP_CMC_71705.md:219` — "results are reported as mean ± standard deviation based on 100 independent simulation runs."
28. `docs/sources/tactic_profiles/step_d/10_disc/3560828.3564006.md:185` — Reti 2022, Table 1 "All Possible Varied Parameter Values": num_honeypots {0,2,4,6,9,10}; movement_time {None,25,50,75,100}; num_hosts {10,50}; one_goal {True,False}; seed_options {1234, 42, 24121997}; agents {careful, standard, aggressive}. **[explicit full-grid design with three named seeds]**
29. `docs/sources/tactic_profiles/step_d/10_disc/3560828.3564006.md:169` — "The most important parameters for this paper are the ones which were decided to be changed and observed. These are the Honeypots in the network and the time until address mutation … The rest of the parameters were fixed throughout all simulations. The network included 256 addresses and two subnets"
30. `docs/sources/tactic_profiles/step_d/6_privesc/herranz2023_surgical_immunization_ad_jnca.md:315` — "For each immunization strategy and each attacker profile, a factorial extensive experiment set was conducted"; L319: "10 different sizes of the initial infection set … 10 different subsets … as infection seeds … For each set of initial parameters, the simulation was repeated 300 times to compensate the randomness inherent in the continuous-time stochastic process … a total of 30,000 simulations"; L338: "MTHC together with its 95% confidence intervals" **[factorial + 300 reps + CIs; AD lateral-movement paper]**
31. `docs/sources/tactic_profiles/step_d/1_recon/Software_Rejuvenation_Meets_Moving_Target_Defense_Modeling_of_Time-Based_Virtual_Machine_Migration_Approach.md:230` — Torquato 2022: "We search for the availability-aware VM migration trigger using sensitivity analysis of transition migTrigger delay on the system availability. We study the steady-state availability while varying VM migration triggers from 30 minutes to 48 hours using a 6-minute (0.1 hours) step." **[explicit single-parameter sweep with range and step]**; L399: "we aim to conduct a comprehensive sensitivity analysis of the other parameters of the models" (future work)
32. `docs/sources/tactic_profiles/step_d/0_cross_tactic_timed_models/1-s2.0-S0306454921007404-main.md:545` — Tripathi 2022 GSPN: "To perform sensitivity analysis for evaluating and comparing steady state probabilities, we vary the strength of preventive measures and responsive measures (at network and host level) and analyze its effect on model evaluation metrics including steady state probability, MTTD and system availability."
33. `docs/sources/tactic_profiles/step_d/0_cross_tactic_timed_models/orojloo2018_cps_stochastic_petri_nets_ietcps.md:63` — "To estimate the availability metric, we need to study the behaviour of the system in a steady state and consider all states of the model as transient states."
34. `docs/sources/tactic_profiles/step_d/0_cross_tactic_timed_models/wu2021_stochastic_evolutionary_game_petri_net.md:273` — "we generally use MTTF to describe the steady-state reliability of the system"
35. `docs/sources/tactic_profiles/step_d/0_cross_tactic_timed_models/madan2004_intrusion_tolerant_quantification_pe.md:191` — "Clearly for the model to be accurate, it is important to estimate accurately the model parameters (i.e., mean sojourn times and the DTMC transition probabilities) … our focus is primarily on developing a methodology" (NB `download_list.md:186` claims Madan "runs sensitivity analysis on rate inaccuracy" — the word "sensitivity" does not appear in the Madan source md; unverified)
36. `docs/sources/tactic_profiles/step_d/download_list.md:186` — "the landmark semi-Markov MTTSF paper: declares per-state sojourn times + runs sensitivity analysis on rate inaccuracy. The direct methodological precedent." [repo annotation]
37. `docs/sources/tactic_profiles/step_c/mcqueen2006_time_to_compromise.md:759` — "We would like to perform a sensitivity analysis to determine…" (future work, confirms extraction L116)
38. `docs/sources/tactic_profiles/step_c/s10270-021-00898-7.md:376` — Xiong 2021: "the SSSP algorithm is deterministic. To perform probabilistic computations, the deterministic algorithm is enveloped in a Monte Carlo simulation. Thus, a large set of graphs is generated"
39. `docs/sources/tactic_profiles/step_d/0_cross_tactic_timed_models/3230833.3232799.md:368` — Johnson 2018 MAL: same Monte Carlo envelope statement ("the SSSP algorithm is deterministic. In…")
40. `docs/sources/tactic_profiles/step_d/5_persist/TSP_CMC_64849.md:316` — Sun 2025 Stackelberg-FlipIt: "The experiment employs 1000 episodes with T = 100 steps per episode and 100 independent trials."
41. `docs/sources/tactic_profiles/step_d/11_lat_movement/586110.586130.md:194` — Zou, Gong, Towsley 2002 Code Red: "how variable each simulation is among the 100 simulation runs of the two-factor model. By using the maximum and minimum values … we derive two envelope curves that contain all these 100 curves … The maximum difference between these two curves is only 0.227%"
42. `docs/sources/tactic_profiles/step_d/11_lat_movement/zou2003_monitoring_early_warning_worms_ccs.md:219` — "Worm propagation is in fact a stochastic process. In order to check if the Kalman filter detection algorithm works well under most cases, we … run the Code Red simulation for 100 times. Fig. 7 shows the upper and lower bounds and the average value"
43. `docs/sources/tactic_profiles/step_d/11_lat_movement/alshaer2012_random_host_mutation_securecomm.md:213` — "In the simulation, every data point is the average of 10 runs, and there are 10% MTs in the network."
44. `docs/sources/tactic_profiles/step_d/10_disc/An_Effective_Address_Mutation_Approach_for_Disrupting_Reconnaissance_Attacks.md:447` — Jafarian 2015 RHM: "All values have been achieved in real scenarios and averaged over 10 runs."
45. `docs/sources/tactic_profiles/step_d/10_disc/file.md:297` — Wang 2017 RDAM: "In the simulation, every data point was taken as the average of 10 runs, and the scanner executed a total of m^E scans."
46. `docs/sources/tactic_profiles/step_d/9_cred_access/1866307.1866328.md:259` — "Average over 10 trials, with one standard deviation shown." (password-transform paper, Figs 5–10 all "average of 10 trials")
47. `docs/sources/tactic_profiles/step_d/6_privesc/The_-Time-to-Compromise_Metric_for_Practical_Cyber_Security_Risk_Estimation.md:410` — Zieger 2018: "Samples: 2000 random vulnerability counts Random range: 0-100 vulnerabilities Rounds for each call: 10 Repetitions: 5" (compute-performance benchmark, not effect replication)
48. `docs/sources/tactic_profiles/step_d/0_cross_tactic_timed_models/1-s2.0-S0045790626000315-main.md:511` — Davies & Macfarlane 2026 ransomware: "execution times together with confidence intervals derived from ten independent trials, providing a statistically grounded view of variability across families."
49. `docs/sources/tactic_profiles/step_d/4_exec/978-1-4614-0977-9.md:1557` — Springer MTD volume (SQLrand chapter): "The users executed, in a round-robin fashion, a set of five queries over 100 trials."
50. `docs/sources/tactic_profiles/step_d/2_resource_dev/RAND_RR1751.md:1128` — "Taking 365 days and 90 days as the likely time intervals (as well as 30 days and 1 day intervals), we performed sensitivity analysis on our data, to assess the percentage of vulnerabilities that died in certain time intervals." (empirical SA on an interval parameter)
51. `docs/sources/tactic_profiles/step_d/2_resource_dev/RAND_RR1751.md:976` — "median survival time of 5.07 years (95 percent confidence interval: 3.71, 7.55)"; L1098: "A 95 percent confidence interval of 5.39 to 8.84 years means we are 95 percent confident that the average lifespan of exploits like those in our sample is between…"
52. `docs/sources/tactic_profiles/step_d/3_initial_access/2024-dbir-data-breach-investigations-report.md:1109` — "This year we have made liberal use of confidence intervals to allow us to analyze smaller sample sizes … Here we define 'small sample' as less than 30 samples." **[an explicit reporting rule]**
53. `docs/sources/tactic_profiles/step_d/1_recon/sec14-paper-durumeric.md:308` — Durumeric 2014 ZMap: "We performed the two scans using ZMap, selecting identical randomization seeds such that the probes from both subnets…" (seed control for comparability)
54. `docs/sources/tactic_profiles/step_d/11_lat_movement/chernikova2023_siidr_epidemiological_ans.md:730` — "we use here a more advanced ABC technique that leverages Sequential Monte Carlo (ABC-SMC)" (parameter estimation, WannaCry fit)
55. `docs/sources/tactic_profiles/step_d/0_cross_tactic_timed_models/1-s2.0-S0951832018304125-main.md:688` — "the average running time of 30 independent runs between the SPPSO algorithm and the traditional PSO" (the mis-downloaded PSO paper; not attacker-timing — flagged in timed_attack_models L54–60)
56. `docs/sources/tactic_profiles/step_d/1_recon/Parameterizing_Moving_Target_Defenses.md:47` — Anderson 2016: "Collins [5] proposes a game theoretic way to assess the effectiveness of MTD. His MTD taxonomy comprises permutation, ephemeralization and replication techniques" (taxonomy, not replication)
57. `docs/sources/tactic_profiles/step_d/0_cross_tactic_timed_models/1-s2.0-S1389128613000856-main.md:27` — Almasizadeh 2013: "The basic assumption of our model is that the time parameter plays the essential role in capturing the nature of an attack process."
58. `docs/sources/tactic_profiles/step_c/mcqueen2006_scada_risk_reduction.md:130` — "It is used to determine steady-state availability" (companion INL report; unread per extraction)
59. `docs/sources/tactic_profiles/step_d/15_impact/TSP_CMC_71705.md:111` — "The hash function H1 takes the current IP and a random seed r to generate a new, unpredictable address." (seed as mechanism, not experimental seed)
60. `docs/sources/gopen_swan_1990_science_of_scientific_writing.md:481` — "in spite of such variance we might still be able to predict earthquakes?" (writing guide; noise hit)

### Census reading (extraction-only survey; census hits are the only primary-text sightings)

- **Formal sensitivity-analysis methods (Sobol / Saltelli / Morris / OAT by name): zero hits in the entire tree.** Every "sensitivity analysis" in the corpus is either (a) a single-parameter sweep with a stated range and step (Torquato #31: 30 min → 48 h at 6-min step; Zhou per extraction 5–100 min; Tripathi #32 varying measure strength), (b) named as future work (McQueen #2/#37, Cho-Ben-Asher #16, Torquato #31 L399), or (c) used loosely for "we varied a parameter" (Zhang 2023 #13/#14, Tay #19, RAND #50).
- **Replication counts stated in primaries:** 10 runs (Al-Shaer 2012 #43, Jafarian 2015 #44, Wang 2017 #45, password paper #46, Davies 2026 #48); 100 runs (TSP_CMC_71705 #26–27, Zou 2002 #41, Zou 2003 #42, Sun 2025 #40 "100 independent trials", SQLrand #49); 300 reps × 100 starting conditions (Herranz 2023 #30); 1000 Monte Carlo graphs (Xiong/MAL, extraction xiong2021 L85). None of the twelve extractions in the brief records a per-cell replication count except Ferguson-Walter's human n and Xiong's 1000 graphs.
- **CIs / dispersion:** mean ± SD + 95% CI + paired t-test (TSP_CMC_71705 #26); 95% CI on MTHC (Herranz #30); CI from 10 trials (Davies #48); min/max envelope over 100 runs (Zou 2002 #41, Zou 2003 #42); one-SD bars over 10 trials (#46); DBIR's small-sample rule (#52). The MTD-specific papers (Al-Shaer, Jafarian, Wang, Reti) report means of 10 runs or per-seed results with no dispersion statement found by the census.
- **Seeds:** Reti 2022 lists three named seeds as a design factor (#28); Durumeric fixes identical seeds for comparability (#53). No other seed convention found.
- **Factorial:** the word appears as a design description only in Herranz 2023 (#30) and as a 2×2 in Ferguson-Walter (extraction mtd_scan_disruption L164–165); Reti's Table 1 (#28) is a full grid without the word.
- **Warm-up / steady state:** "steady state" appears only as the analytical solution regime of Markov / SPN / GSPN models (Madan, Orojloo #33, Wu #34, Tripathi #32, Outkin #17); no discrete-event-simulation warm-up convention appears anywhere.
- **The one paper-side "convention" sentence about simulation methodology:** Cho 2020 survey (#12): simulation's "experimental capability to conduct sensitivity analysis by varying the values of key design parameters" is its stated advantage over analytical models — a survey-level statement that sensitivity-by-parameter-variation is what simulation studies are for.
