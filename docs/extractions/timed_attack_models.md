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
> ([`../notes/2026-07-04_operational_validation_the_bar.md`](../notes/2026-07-04_operational_validation_the_bar.md)).
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

- **Citation keys**: `katsikeas2020_corelang` (Katsikeas, Hacks, Johnson,
  Ekstedt, Lagerström et al., *A probabilistic attack simulation language for the
  IT domain* (coreLang), GraMSec 2020). *(Folder-0 keys — `johnson2018_mal`,
  `holm2015_p2cysemol`, `johnson2016_pwnpr3d`, `widel2023_mal`,
  `katsikeas2022_vehiclelang`, `madan2004`, `almasizadeh2013`, `orojloo2018`,
  `zhou2019`, `wu2021`, `liu2019`, `lalropuia2019`, `tripathi2022` — added on
  folder-0 dissection.)*
- **Pages cited from**: coreLang §"MAL basics" (attack steps + probability
  distributions + defenses).

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

**Maps to:** [`08_defense-impairment`](../tactic_profiles/08_defense-impairment.md)
§4 (formal precedent for modelling *defences the attacker must disable/bypass* as
gating entities — and for declaring a per-step effort distribution rather than
measuring it) + the method note (MAL-family declared per-step TTC — the same
register as [`ling2023`](ling2023.md), [`xiong2021`](xiong2021.md)).

**Disposition for this thesis:** verified [fetched] — method precedent (declared
per-step distributions + defenses-as-gates). No cyber-tactic dwell value; a
*construction* to cite, not a number to transplant.

<!-- Folder-0 blocks (johnson2018 MAL, P2CySeMoL, pwnPr3d, Widel MAL formalism,
     VehicleLang, Madan 2004, Almasizadeh 2013, Orojloo 2018, Zhou 2019, Wu 2021,
     Liu 2019, Lalropuia 2019, Tripathi 2022) appended when folder 0 is dissected. -->

## Open questions / things to verify

- Every model here **declares** its per-step/per-state timing (expert/literature/
  CVSS-elicited) — none measures per-ATT&CK-tactic dwell. They are the *precedent*
  that legitimises our declare-and-sweep, and the ICS/CPS ones are method-only
  (domain values do not transfer to cyber tactics).

## Out of scope for this thesis

MAL language syntax/semantics detail; the ICS/CPS/nuclear domain physics; each
model's solver internals. The load-bearing part is the shared method: declare a
per-step time distribution, then sweep it.
