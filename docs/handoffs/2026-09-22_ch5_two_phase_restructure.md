---
status: open                  # executes register E1 (with E7 and E10 pointers); Marc's rulings R1–R4 owed before the tex moves
created: 2026-09-22
executes: docs/implementation/pipeline/ogasp/supervisor_decision_register.md §E1, §E7, §E10
companions: 2026-09-20_ch5_s52_s54_results_context.md (the figure records in its §8 stand; its §2–§4 and §6 are superseded in shape by this file), 2026-09-09_ch5_experiments_design.md (the funnel §8, the property-to-measurement map §9 and the debt ledger stand), 2026-09-22_ch5_defended_corpus_schemes_intervals_mtdshield.md (the corpus this chapter reads), 2026-09-22_terminology_needs_basis_sweep.md (the words), 2026-09-22_metrics_provenance_and_instrumentation.md (the metrics)
---

# Restructure chapter 5's results into the two phases the supervisor ruled: the APT attacker model against the baseline attacker without defence, then the defences against the APT attacker model

## State of play

**What stands in the tex** (`docs/thesis/dissertation.tex`, 2026-09-22):

| § | Heading | Line | Content |
|---|---|---|---|
| 5 | Evaluation | 5075 | roadmap placeholder |
| 5.1 | Experimental setup | 5456 | four run-in units, Tables 5.1–5.2; through pass 6 (2026-09-20) |
| 5.2 | Behaviour of the APT attacker model | 6067 | placeholder |
| 5.2.1 | Without defence | 6185 | Figure 5.1 (campaign openings), Table 5.3 (unopposed summary); the divergence and 60 000 s readings are body sentences owed |
| 5.2.2 | Response to disruption | 6452 | head paragraph in DRAFT STATE; Figure 5.2 (disruption response, ratio form) |
| 5.3 | Defence effectiveness | 6745 | placeholder |
| 5.3.1 | Defence mechanisms and execution schemes | 6771 | Figure 5.3, Table 5.4 |
| 5.3.2 | Effect of the attacker model | 6861 | Figure 5.4 (cross-arm), Table 5.5 (orderings) |
| 5.3.3 | Comparison with prior evaluations | 6909 | Table 5.6 (lineage claims re-run) |
| 5.4 | Defence efficiency | 6963 | placeholder; Figures 5.5 (frontier), 5.6 (time split), Table 5.7 (cost) |

Every float is generated (`docs/thesis/FLOATS.md`) from `data/results/ch5_s531_unopposed/` and `data/results/ch5_defended/` at 100 seeds. No results prose has been drafted beyond the §5.2.2 head; the results-paragraph shape is settled (results context §3) and stands.

**What the supervisor ruled (E1, 2026-09-22).** Two phases, read from the APT attacker's perspective: (1) *no MTD* — the APT attacker model compared with the baseline attacker; (2) *MTD* — the existing defences against the APT attacker model, the baseline attacker as a reference line inside the same floats, effectiveness and efficiency merged, sub-subsections by the purpose of each experiment. The prior-evaluations comparison dissolves into phase two (E6: run their configurations, add Tay's selector as a scheme). Rankings are based on the APT attacker model (E7).

**What this overturns, named.** The 2026-09-20 ruling that the three-way split (attacker run / what the defences achieve / what it costs) was right (results context §2), and the five headings approved the same day (§4). Both were Marc's rulings on the session's proposal; the supervisor's reading of the headings on the page is the evidence that overturns them. The design handoff's funnel (one run set answers two questions) is unaffected — it is exactly what the two phases do.

## Recommended approach

### 1. The shape

```
5    Evaluation
5.1  Experimental setup                                   (as is; numbers justified by the setup handoff)
5.2  [phase one — no defence]  the APT attacker model against the baseline attacker
       body: Table 5.3 with the stealth and detectability columns reinstated (metrics handoff);
             Figure 5.1 in colour, panel (b) as bars (figure handoff);
             the pairwise-divergence sentence; the 60 000 s pace sentence (ruled 2026-09-22, §8e)
5.3  [phase two — defence]     the defences against the APT attacker model
       5.3.1  Response to disruption        — what one deployment does to each attacker (Figure 5.2)   [R2]
       5.3.2  Defence mechanisms across the deployment interval
                — the sweep: the field's success metric against interval, both attackers,
                  aggregated by the layer each mechanism rewrites (body); per-mechanism and
                  per-profile panels in a new appendix section
       5.3.3  Execution schemes and MTDShield — random, alternative, MTDShield as released
                ("no AI versus AI"); absorbs the prior-evaluations comparison
       5.3.4  Cost                          — what §5.4 carried, if kept as a sub-subsection   [R3]
       the ranking table, based on the APT attacker model (E7), sits with 5.3.2 or closes 5.3
```

Two phases, not three sections, so the chapter's table of contents reads: the experiment; the model against the baseline; the defences against the model.

### 2. Headings — proposals for Marc's ruling (R1)

Audited against Marc's rules (sentence case; no acronym but APT, with MTD already licensed by ch3's headings; two to six words; a noun phrase naming the object or factor; no claim; the model's name is not a flourish — under E2 it is now the chapter 4 title) and against the corpus form (results context §4: siblings name the same kind of thing).

| § | Option (a) — recommended | Option (b) | Why (a) |
|---|---|---|---|
| 5.2 | **APT attacker model against the baseline attacker** | Comparison of the two attackers without defence | Jin's own form ("this APT attacker versus baseline attacker"); names both objects compared and nothing else; *against* is the chapter's verb for a contest, as ch3 §3.3 already uses it |
| 5.3 | **Defence mechanisms against the APT attacker model** | MTD against the APT attacker model | *defence mechanism* is the ratified noun (2026-09-07); it pairs with 5.2 in form (X against Y) and keeps the attacker as the object of the chapter |
| 5.3.1 | Response to disruption | — | ratified 2026-09-20; the quantity, in the ratified word |
| 5.3.2 | **Defence mechanisms across the deployment interval** | Impact of the deployment interval (Ho's factor form) | names the factor swept; *deployment interval* is the ratified row |
| 5.3.3 | **Execution schemes and MTDShield** | Deployment strategies (the ratified covering term for the five) | (b) is shorter and already ratified; (a) says what is in the section — Marc's call |
| 5.3.4 | **Cost of defence** | What the defence costs | only if R3 keeps a sub-subsection |

The current "Behaviour of the APT attacker model" fails on Jin's reading: it names what the whole chapter is about, so it cannot title one section of it.

### 3. Float moves

| Float | Today | Under the new shape |
|---|---|---|
| Fig 5.1 campaign openings | 5.2.1 | 5.2; colour and bars per the figure handoff; regenerated at 1 000 seeds |
| Tab 5.3 unopposed summary | 5.2.1 | 5.2; two columns added (stealth spacing, detectability) — metrics handoff |
| Fig 5.2 disruption response | 5.2.2 | 5.3.1; a key for the hollow circles |
| Fig 5.3 suppression by profile | 5.3.1 | **retire** in this form: its metric name goes (E2/E3) and its two intervals become the sweep; the per-profile reading moves to the appendix panels |
| Tab 5.4 conditions | 5.3.1 | 5.3.2 or 5.3.3, at the interval(s) the body reports, on the field's metric names; the baseline attacker as rows beside the model |
| Fig 5.4 cross-arm | 5.3.2 | becomes the **body sweep figure**: metric against interval, both attackers, layer-aggregated |
| Tab 5.5 orderings | 5.3.2 | with 5.3.2: ranks based on the model, the baseline second (E7); footnote gone |
| Tab 5.6 lineage claims | 5.3.3 | **dissolve** into 5.3.3's prose (one paragraph: the lineage's own disagreement reproduced, one attacker each) or drop — R4 |
| Fig 5.5 frontier | 5.4 | **retire** (Marc: "I don't even know what this means"); the occupancy quantity, if kept, is a table column |
| Fig 5.6 time split | 5.4 | keep only if R3 keeps cost; otherwise its two shares are Table 5.7 columns |
| Tab 5.7 cost | 5.4 | 5.3.4 if kept |

Labels stay (`sec:attacker-in-operation`, `subsec:aio-unopposed`, `subsec:aio-disruption`, `sec:effectiveness`, `subsec:eff-*`, `sec:efficiency`) so every `\ref` stands; `sec:efficiency` becomes the label of 5.3.4 or is removed with its section.

### 4. Order of work

1. Marc rules R1–R4 (one sitting).
2. The corpus handoff runs (the sweep, the schemes, MTDShield) — independent of this file; start it first, it is the long pole.
3. The terminology and metrics handoffs settle the words and the metric names — the float generators take both through `tools/_ch5_style.py`'s label map and the analyser.
4. Move the tex: headings, section comments (rewrite the "PROPERTY -> SUBSECTION" map at l.~6047 and every "fed by" wiring comment), floats; update `FLOATS.md`; rebuild; check the ch6 "fed by" comments still point at live sections.
5. Append a dated banner to the results context (done in this commit) and re-cut its §6 opening slots for the two phases when drafting starts.
6. Drafting follows the pipeline: Marc dictates each unit; the results-paragraph shape of results context §3.

### 5. The discussion (E10)

Two set-ups Jin named are appended to the affinity board handoff (its §9): the model is harder to detect while slower and less successful — why APT attacker modelling matters; and the effective defence differs by attacker — no single solution, more research. Both are already on the board as mini-hypotheses; the note only records that the supervisor has now named them as the discussion's spine.

## Rulings owed (Marc)

- **R1** the heading set (§2 table).
- **R2** where the response-to-disruption reading sits: head of phase two (recommended — Jin's "probably, yeah"; it is what one deployment does, so it belongs with the defences) or the close of phase one.
- **R3** does cost survive as a sub-subsection (time lost to MTD; share of run under reconfiguration), as columns of one table, or not at all. Recommendation: columns; the cost story is one paragraph.
- **R4** the fate of Table 5.6 and the opportunistic-objective arm: a paragraph in 5.3.3 (recommended) or dropped.

## Validation gate

Build clean; the chapter's contents page reads as two phases under one setup; no heading contains *effectiveness*, *efficiency* or *behaviour*; every float in `FLOATS.md` has a live position and every retired one is struck through with its reason; the results context carries the 2026-09-22 banner; the ch6 "fed by" comments point at live labels; `grep -c 'Placeholder' ` on ch5 is unchanged or lower.

## Hard constraints

- Nothing here drafts prose: Marc dictates every unit (drafting_pipeline.md).
- The frame of results context §5 (modelling language, the antecedent rule, the vocabulary table) stands, with its vocabulary re-keyed by the terminology handoff.
- No number reaches the page except from a tracked artefact through a generator, at the reported seed count.
- Branch and commit rules: `docs/workflows/session_workflow.md`.

## Reading list

- `docs/handoffs/2026-09-20_ch5_s52_s54_results_context.md` — §3 (paragraph shape), §5 (frame), §8 (every figure's record).
- `docs/handoffs/2026-09-09_ch5_experiments_design.md` — §8 the funnel, §9 the property-to-measurement map, the debt ledger (l.~2526).
- `docs/thesis/FLOATS.md` — every float's generator.
- `docs/workflows/evaluation_conventions.md` §b, §e, §f — results organised by one axis; the results sentence; the funnel.
- `docs/implementation/pipeline/ogasp/supervisor_decision_register.md` §E1–§E11.

## Out of scope

The words (terminology handoff); the metric definitions and Table 5.2 (metrics handoff); the runs (corpus handoff); the figures' redesign (figure handoff); ch6 drafting.
