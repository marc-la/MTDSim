# Timed attack models — declared per-step/per-state timing precedents (extraction notes)

> A consolidated bundle of **formal attacker-timing models** — MAL-family attack
> languages (coreLang, MAL, VehicleLang, pwnPr3d, P2CySeMoL, the MAL formalism)
> and semi-Markov / SPN / CTMC attack-process models (Madan, Almasizadeh, Orojloo,
> Zhou, Wu, Liu, Lalropuia, Tripathi). Extracted **as the Step-F "declare + justify
> + sweep" method precedent** that parameterises any Tier-3 tactic — *not* as
> sources of cyber-tactic dwell values. Their shared move is exactly ours:
> **assign a probability distribution / sojourn time to each attack step or state,
> from expert/literature elicitation, then run sensitivity analysis.** They are the
> field norm the operational-validation note claims
> ([`../notes/2026-07-04_operational_validation_the_bar.md`](../../notes/ch4_methods/operational_validation.md)).
> Source files (gitignored): `8_defence_impair/GraMSec_2020_paper_7.md` (coreLang);
> `0_cross_tactic_timed_models/*.md` (the rest — appended when folder 0 is dissected).

### Relevance class

**M** (method) — the declare-a-time-per-step precedent + sensitivity-sweep
discipline. Several are ICS/CPS/nuclear/chemical domain: precedents for the
*method*, never for cyber-tactic values.

### Used in lit review

The method note (declare-and-sweep is the field norm); Step-F justification that a
declared per-state dwell + sweep is a recognised, not ad-hoc, construction;
per-tactic §4 rows where a MAL DSL gives a technique a structural/timing shape.

## Bibliographic anchor

- **Citation keys**: `katsikeas2020_corelang` (coreLang, GraMSec 2020);
  `madan2004` (Madan, Goseva-Popstojanova, Vaidyanathan, Trivedi, *Modeling &
  quantifying security attributes of intrusion-tolerant systems*, Performance
  Evaluation 56, 2004); `johnson2018_mal` (Johnson, Lagerström, Ekstedt, *A Meta
  Language for Threat Modeling and Attack Simulations*, ARES'18);
  `holm2015_p2cysemol` (Holm et al., *P2CySeMoL*, IEEE TDSC 12(6), 2015);
  `johnson2016_pwnpr3d` (Johnson, Vernotte, Ekstedt, Lagerström, *pwnPr3d*,
  ARES'16); `widel2023_mal` (Wideł et al., *The MAL – A Formal Description*,
  Computers & Security 130, 2023); `katsikeas2022_vehiclelang` (VehicleLang,
  Computers & Security 117, 2022); `almasizadeh2013` (Almasizadeh, Azgomi, *A
  stochastic model of attack process*, Computer Networks 57(10), 2013);
  `orojloo2018` (Orojloo, Azgomi, *Security of CPS using SPN*, IET Cyber-Physical
  Systems 3(2), 2018); `zhou2019` (Zhou, Reniers, Zhang, *Petri-net based attack
  time analysis*, Comp. & Chem. Eng. 130, 2019); `wu2021` (Wu et al., *Stochastic
  Evolutionary Game SPN*, Security & Comm. Networks, 2021); `liu2019` (Liu, Xing,
  Zhou, *Probabilistic modeling of sequential cyber-attacks*, Engineering Reports
  1(4), 2019); `tripathi2022` (Tripathi et al., *GSPN NPP*, Annals of Nuclear
  Energy 168, 2022).
- **Pages cited from**: coreLang §"MAL basics"; Madan Abstract + §1/§4; Johnson
  2018 §3; Wideł 2023 (`1-s2.0-S0167404823001943`) Abstract; P2CySeMoL/pwnPr3d
  Abstracts; Almasizadeh Abstract; Orojloo §MTTF; Zhou Abstract + surveillance-interval
  sweep; Wu §5.1.3 (MTTR); Liu Abstract (CTMC/SMP); Tripathi Abstract (GSPN
  mean-time-to-disrupt).

> **⚠ Two Step-D file/manifest mismatches found on reading — flagged, not folded in:**
> (1) `1-s2.0-S0951832018304125-main.md` (folder 0) is **not** Lalropuia & Gupta's
> CPA stochastic-game paper the manifest intended — the saved file is *"An improved
> particle swarm optimization algorithm for the reliability-redundancy allocation
> problem"* (a reliability-engineering / PSO optimisation paper with **no
> attacker-timing content**). The wrong RESS article was downloaded; `lalropuia2019`
> is therefore **not** extracted here (re-fetch needed for Marc). (2)
> `1-s2.0-S0045790626000315-main.md` (mis-filed under folder 0) is **Davies &
> Macfarlane 2026, ransomware performance benchmarking** — routed to
> [`ransomware_timing`](ransomware_timing.md) / [`15_impact`](../../notes/ch4_methods/tactic_profiles/15_impact.md),
> not a cross-tactic timed model.

## Relevant artefacts

### coreLang 2020 — MAL attack steps carry probability distributions; defenses are gates

**Source locator:** §"MAL basics" (assets, attack steps, defenses, probability
distributions)

**Paraphrase:** coreLang is a MAL-based domain-specific language for probabilistic
attack simulation over IT models [fetched]. Structure: `assets` contain `attack
steps` (OR/AND-composed into attack graphs); crucially **"probability
distributions can be assigned to the attack steps in order to represent the effort
needed to complete the related attack step"** — i.e. a *declared* per-step
time/effort distribution, elicited from "existing IT attack studies". `defenses`
are entities that **block connected attack steps when TRUE** — a formal model of
"the defences an attacker must bypass", which is precisely the
defense-impairment target.

**Maps to:** [`08_defense-impairment`](../../notes/ch4_methods/tactic_profiles/08_defense-impairment.md)
§4 (formal precedent for modelling *defences the attacker must disable/bypass* as
gating entities — and for declaring a per-step effort distribution rather than
measuring it) + the method note (MAL-family declared per-step TTC — the same
register as [`ling2023`](ling2023.md), [`xiong2021`](xiong2021.md)).

**Disposition for this thesis:** verified [fetched] — method precedent (declared
per-step distributions + defenses-as-gates). No cyber-tactic dwell value; a
*construction* to cite, not a number to transplant.

---

### Madan 2004 — the landmark: semi-Markov MTTSF from declared per-state sojourn times

**Source locator:** Abstract; §1 (SMP rationale); §4 (MTTSF via absorbing states);
§"mean sojourn time" (analysis depends only on the mean)

**Paraphrase:** **the direct methodological precedent** for this thesis's timing
layer [fetched]. Models an intrusion + intrusion-tolerant response (SITAR) as a
**semi-Markov process** (SMP — chosen precisely because "some of the sojourn time
distribution functions may be non-exponential"). Makes security-failure states
**absorbing** and computes **MTTSF (mean time to security failure)**, analogous to
MTTF. Load-bearing: "the analysis carried out in this paper depends only on the
**mean sojourn time** and is independent of the actual sojourn time distributions"
(for steady-state) — i.e. **you declare a mean per-state dwell, and the aggregate
metric follows.** This is exactly our per-state declared-dwell → emergent-timeline
construction, from 2004.

**Maps to:** the method note ([`../notes/2026-07-04_operational_validation_the_bar.md`](../../notes/ch4_methods/operational_validation.md))
— the canonical precedent that declaring per-state sojourn times and solving for an
aggregate security metric is a recognised technique (and that the *mean* is what
matters, licensing shape-not-scale).

**Disposition for this thesis:** verified [fetched] — the landmark precedent.
Declares per-state means, does not measure cyber-tactic dwell; the *construction*
is the contribution to cite.

---

### MAL family — declared per-step/asset TTC over generated attack graphs

**Source locator:** Johnson 2018 Abstract + §3 (MAL formalism); P2CySeMoL Abstract;
pwnPr3d Abstract

**Paraphrase:** [all fetched] the Meta Attack Language lineage — each **declares a
per-attack-step time-to-compromise distribution** and computes an aggregate TTC
over an auto-generated attack graph:
- **Johnson 2018 (MAL):** the foundational meta-language; a simulation yields "a
  probabilistic estimate of the **time to compromise** each attack step"; separates
  generic domain attack-logic from a specific system instance.
- **P2CySeMoL (Holm 2015):** attack-graph TTC where per-step probabilities are
  elicited from "literature, domain experts, surveys, observations, experiments and
  case studies" (a *stated provenance* — the honest badging our method also uses),
  while flagging that expert estimates are valid only for their time/scope/competence.
- **pwnPr3d (Johnson 2016):** "generates probability **distributions over the Time
  To Compromise (TTC) for each asset**"; closed meta-model (MOF-layered), like
  coreLang.
- *(VehicleLang, Widel-cose MAL formalism — same family: MAL-based per-step TTC /
  formal TTC semantics.)*

**Maps to:** the method note (declared per-technique/step TTC is the field norm —
the register [`ling2023`](ling2023.md)/[`xiong2021`](xiong2021.md) already anchor;
folder-0 broadens the precedent base) + Tier-3 justification.

**Disposition for this thesis:** verified [fetched] — method precedent; per-step
TTC, not per-ATT&CK-tactic dwell.

---

### Semi-Markov / SPN / CTMC attack-process cluster — declared sojourn + MTTSF/MTTF + interval sweep

**Source locator:** Almasizadeh Abstract; Orojloo §"mean holding time"/§MTTF; Zhou
Abstract + §(surveillance-interval sweep); (Wu, Liu, Lalropuia, Tripathi — same
family)

**Paraphrase:** [all fetched] a cluster of stochastic attack-process models, all
executing the **declare-per-state-time → solve-for-aggregate → sweep** move:
- **Almasizadeh 2013:** a **semi-Markov chain** with "probability distributions
  defined and assigned to transitions" for attacker actions + system reactions;
  solves for MTTSF + steady-state security. "the time parameter plays the essential
  role."
- **Orojloo 2018 (CPS):** SPN → semi-Markov; declares **mean holding time per state**
  + transition probabilities (input-parameter table); computes **MTTF** (absorbing
  states) and availability (adds a restoration transition 1/Tr — the *reset* rate).
- **Zhou 2019 (chemical TCPN):** timed coloured Petri net for attack-completion
  time; **sweeps the surveillance/inspection interval from 5 to 100 minutes** and
  reads off security-failure probability — a direct analogue of our
  reset-interval sweep (a defensive "move" at interval X vs the attack duration).
- **Wu 2021 (SPN + evolutionary game):** computes attack success rate, **average
  attack time and mean-time-to-repair (MTTR)** from declared rates (§5.1.3).
- **Liu 2019 (sequential cyber-attacks):** **CTMC** (exponential transitions) +
  **semi-Markov** (arbitrary transition-time distributions) for sequence-dependent
  attacks; Trojan-banking case.
- **Tripathi 2022 (GSPN, NPP):** quantifies **mean-time-to-disrupt** + availability
  under combined preventive/reactive measures (nuclear-plant CPS).
- *(All ICS/CPS/nuclear/chemical or generic — precedents for the METHOD (declare
  per-state time, solve for MTTSF/MTTF/MTTR, sweep the interval), not for
  cyber-tactic values. Lalropuia's CPA stochastic-game — a further CTMC precedent —
  could NOT be verified: the saved file was the wrong article (see the mismatch
  flag above).)*

**Maps to:** the method note (declare-and-sweep, incl. **sweeping the
defensive-interval** — Zhou's surveillance interval and Orojloo's restoration rate
are the reset-interval analogue our §3/§5 sweep uses) + the sensitivity discipline.

**Disposition for this thesis:** verified [fetched] — method precedents. The
ICS/CPS/chemical/nuclear domains mean the *values* do not transfer; the
**construction** (declare per-state time, solve, sweep the interval) does, and it
is exactly what this thesis executes.

## Open questions / things to verify

- Every model here **declares** its per-step/per-state timing (expert/literature/
  CVSS-elicited) — none measures per-ATT&CK-tactic dwell. They are the *precedent*
  that legitimises our declare-and-sweep, and the ICS/CPS ones are method-only
  (domain values do not transfer to cyber tactics).

## Out of scope for this thesis

MAL language syntax/semantics detail; the ICS/CPS/nuclear domain physics; each
model's solver internals. The load-bearing part is the shared method: declare a
per-step time distribution, then sweep it.
