---
status: open                  # executes register E3 and E4; Marc's disposition pass on the §1 table owed; owns the internal-MTTC finding the README carried unowned since 2026-08-05
created: 2026-09-22
executes: docs/implementation/pipeline/ogasp/supervisor_decision_register.md §E3, §E4
companions: 2026-09-22_terminology_needs_basis_sweep.md (the word *suppression*), 2026-09-22_ch5_two_phase_restructure.md (where the reinstated columns land), 2026-09-22_ch5_defended_corpus_schemes_intervals_mtdshield.md (the analyser that computes every row)
---

# Give every metric a source — a citation, or a methodology definition with why it is needed — and put stealth and detectability back beside the no-defence numbers

## State of play

**The ruling (E3, E4).** For each metric the supervisor wants the reference (MTTC, NCR and the like, formulas referenced); a new metric must be in the methodology with the full detail of how it is calculated and *why* — it must explain something the existing metrics cannot. Stealth is the licensed exemplar (no simulator computes it; APTs are defined by remaining undetected). *Suppression* fails the test (attack success rate before and after). The stealth and detectability readings return to Table 5.3, grouped with hosts reached and delay to first compromise so the "worse" numbers are read with the property that explains them.

**Table 5.2 today** (`docs/thesis/tables/tab_5-1b_metrics.tex`, ten rows, no source column; the file's comment trail records the 2026-09-18/20 rulings that produced it, including Marc's own question "are we not carrying over the names of our lineage's metrics?" — the answer was recorded but not actioned).

### 1. The provenance triage — Marc's disposition pass

Third column is the session's reading of the extractions and Table 3.1; verify each locator before it reaches the tex.

| Table 5.2 row | Field counterpart (Table 3.1 / extraction) | Proposed disposition |
|---|---|---|
| Target reached | attack success probability / rate — Evans, Cho, Kim, Masud; Ho, Tay (ASR); Brown's scenario 2 (*"reach a specific target host"*, brown2023 p.4) | **cite** as attack success rate at the targeted objective; keep the plain name in the float, the field's name and cite in Table 5.2 |
| Runs with no compromise | none as a named metric | **define or fold**: it is the complement of "any success" — fold into the success row (a second rate), or define in the ch4 unit with why (the profiles fail to gain a first foothold at a rate the baseline never does) |
| Blocked fraction | Brown's *attack actions blocked* is his interrupt, not this (attribution removed 2026-09-20) | **define** in the ch4 unit (share of actions failing a precondition after a deployment) with why, or **drop** — it is diagnostic, and §5.3.1 already reads the mechanism |
| Delay to first compromise | **mean time to compromise** — McQueen 2006; Zhang, Ho, Tay (the lineage's primary metric) | **report as MTTC**, checkpoint stated (first host; Zhang's is at NCR 0.8). See §2 below: the thesis's MTTC must be defined explicitly and never be `evaluation.py`'s `time_to_compromise` |
| Hosts reached | **network / host compromise ratio** — Zhang, Ho, Tay | **report as NCR** (hosts / 50 at the time limit), cited; the 2026-09-18 objection (a count vs a checkpoint ratio) is answered by defining the checkpoint as the time limit |
| Suppression | none | **retire**; the before/after pair (no defence, defence) on NCR or ASR, or the relative reduction unnamed |
| Actions per host reached | Brown's *attempts required to compromise* | **cite** (already attributed) |
| Successes per host reached | none | **define or drop** |
| Time lost to MTD | Zhang's per-interruption time penalty is the nearest (zhang2023 p.31) | **define** in the ch4 unit if cost survives the restructure (R3), else drop |
| Share of run under reconfiguration | downtime family — Hong's NVDT, Tay's node-replacement downtime; MEF / TSLM (Ho) | **cite** as the downtime measure, or drop with cost |

**The two to reinstate (E4)** — both exist as readers and have run:

| Metric | Record | Headline on the record | Caveats that ride with it |
|---|---|---|---|
| **Detectability** (exposure level) | `stealth_exposure_metric.md` (R1: the increment fires on a verb invocation; R2: verb-level tiers both arms) | four of five profiles at mean 0.40 against the baseline's 0.72 (`stealth_spacing_diagnostic.md`) | cross-clock; the baseline's record stops at ~77 % of the horizon; a large part of the contrast is present before decay |
| **Stealth** as inter-invocation spacing | `stealth_spacing_diagnostic.md` (not pre-registered — a diagnostic re-read) | four of five profiles space verb invocations 1.5–1.8× further apart, CI-disjoint; the fifth ($c_4$) denser; an ablation attributes the margin to the non-action tactics | per-vulnerability row count (D4) unresolved — state at invocation granularity, show the other reading beside it (`stealth_dutycycle.md` §8) |

Both are *observations* of the no-defence arm (conventions §f); the axis-5 badge stays NOT ADDRESSED (a reader, not a state) and chapter 6 says so. Both need recomputing on the 1 000-seed no-defence corpus (corpus handoff) and a hand trace on a four-host network (V1) before they reach the page.

### 2. The internal-MTTC finding, now owned here

`docs/handoffs/README.md` has carried since 2026-08-05 "one finding with no owner": `mtdnetwork/statistic/evaluation.py:110` computes attack-action time over the *number of attack actions* — a mean action duration — and ranks IP shuffle best and OS diversity below no defence (`attacker_read_surface.md` §(m1)). Disposition proposed: the thesis's MTTC is **defined in the ch4 unit as the time to the first host compromised** (the movement arm's own definition, sound), computed by the chapter's analyser on both arms, and `evaluation.py`'s quantity is never reported; `metrics_semantics.md` §(a) gains a one-paragraph note that the reported MTTC is not that function, and `project_context.md`'s "primary metric is internal MTTC" sentence is corrected.

### 3. The chapter 4 unit

Marc's proposal: a unit after §4.4.4, "instrumenting MTDSim". Two placements:

- (a) **§4.4.5** under L4 — the metrics as the last thing the join declares.
- (b) **§4.5** as its own section, heading *Metrics* (or *Instrumenting MTDSim*, Marc's phrase) — recommended: the metrics are not part of the join, and §5.1's Metrics unit then has one place to point (the antecedent rule: chapter 5 speaks only in chapter 4's words).

Per metric: the field's name; the definition in the formalism's symbols where one applies (the marking, the visit stream, $\tau_p$); what it captures; why the existing metrics do not; the citation or the reason it is new. The four §5.2 instruments (campaign coverage, opening variety, profile divergence, response to disruption) are declared here too, briefly — E3 does not exempt them, and the 2026-09-18 instrument/metric split then needs no separate register. Every new metric gets its hand trace (V1), recorded in a small validation table in the appendix or the record.

Table 5.2 gains a **Source** column: a citation, or the §4.5 pointer.

## Rulings owed (Marc)

The §1 disposition column, one pass; the placement and heading of the unit (§3); whether the lineage names (MTTC, NCR, ASR) are adopted on the floats or only in Table 5.2's Source column.

## Validation gate

Every Table 5.2 row has a Source; every row marked *define* has a definition-and-why paragraph in the ch4 unit; *suppression* appears nowhere in the tex body or floats; Table 5.3 carries the two reinstated columns at 1 000 seeds with their caveats in the caption or one body sentence; each new metric has a hand-trace record; `metrics_semantics.md` and `project_context.md` corrected; build clean.

## Hard constraints

- The claim ceiling: the reinstated columns are observations; no stealth *state* is claimed; the badge does not move.
- Numbers reach the page only through the analyser and a generator at the reported seed count.
- Literature conventions: definition before use; the field's name where the quantity is the field's (`literature_conventions.md`).

## Reading list

- `docs/thesis/tables/tab_5-1b_metrics.tex` — the comment trail is the record of every prior ruling on this table.
- `docs/implementation/metrics_semantics.md` §(a), §(d); `docs/implementation/attacker_read_surface.md` §(m1).
- `docs/implementation/pipeline/ogasp/measurement_suite.md`; `stealth_spacing_diagnostic.md`; `stealth_exposure_metric.md`; `stealth_dutycycle.md` §8.
- `docs/thesis/dissertation.tex` l.2380–2500 — Table 3.1 and its citations.
- `docs/sources/extractions/{brown2023,zhang2023,ho2024,tay2024}.md` — the metric definitions and locators.
- `docs/workflows/literature_conventions.md` — metric definition-before-use.

## Out of scope

The word sweep (terminology handoff); the runs (corpus handoff); where the columns sit in the chapter (restructure handoff).
