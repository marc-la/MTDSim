---
status: open                  # executes register E8; Parts A, B, C BUILT 2026-09-25 (Figure 4.1 and the two zooms scrutinised clean; the L-label/term sweep applied); captions DRAFT STATE; D carried; F2, F3 and the ledger's rulings owed
created: 2026-09-22
updated: 2026-09-25
executes: docs/implementation/pipeline/ogasp/supervisor_decision_register.md §E8
companions: ../workflows/terminology.md (row 47 to correct: L4 is the join; the L-labels retire under B), ../workflows/figure_table_conventions.md §(n) (the SVG route), .claude/skills/scrutinise-figure/ (SKILL.md schematic variant + diagram_best_practice.md — the acceptance test), ../implementation/evaluation_anatomies/_overview_figures_survey.md (corpus exemplars)
---

# The chapter 4 overview figure — design plan (primary), the L-label retirement and the zoom family (secondary), and the chapter 5 fixes (carried)

## State of play

**The ruling (E8, 2026-09-22).** "Getting this figure right is like explaining
half of your work." A high-level box figure at the chapter head — the boxes and
how they link, nothing else — and each sub-component as a zoom in its own
section. **The supervisor again, relayed by Marc 2026-09-25:** still too
complicated, the labels try to do too much, not intuitive for the audience, the
long caption gives it away; the levels are not levels, and is MTDSim a level?

**The scrutiny (2026-09-25, below the plan)** upheld every point with four
independent reviewers and a 21-test pitfall catalogue: 21 of 21 hit, five
blocking. The figure is a worked example, not an overview; it tells half the
method (no defences, baseline attacker or measure); it calls L4 MTDSim where
§4.4 says L4 is the join; about sixteen of its words have no antecedent; the
L-labels name a layered structure the pipeline does not have.

## Rulings taken 2026-09-25 (Marc, on the scrutiny)

- **F1 — the box set:** the Ferraz 2024 Fig. 2 pattern, with MTDSim as a
  container — "yeah we can do that". Keep it simple: boxes and how they link.
- **F4 — the L-labels go** ("we should get rid of the old labels"), from the
  figure and the prose. What replaces them is secondary (Part B; F4b owed).
- **F5 — the figure shows the defences, the baseline attacker and the
  metrics** ("OK let's do that").
- **The zoom family** (one figure per part, beside its section) stays, as
  secondary to the head figure (Part C).

## Rulings still owed

- **F4b — what the sections are called once the L-labels go** (Part B; the
  recommendation and Marc's "Process 1, Process 2" alternative are set out there).
- **F2** — the colour exception for Figure 5.1(a) (Part D).
- **F3** — whether the old worked-example ladder also survives whole as an
  appendix figure, or only as the two zooms of Part C (recommended: the zooms
  only; Appendix B already carries a flow exemplar, `fig_B-1a_gap_flow_exemplar`).

- **From the Part A build (2026-09-25), four items only Marc can settle:**
  - **A3 amended?** The figure carries *Petri nets* under *Profile nets*: all
    three round-1 readers could not place "profile nets", and the term has its
    antecedent in the chapter 4 opener (l.4165). A3 banned *Petri* to keep net
    notation (token, fire, place) off the head figure; the recommendation is to
    keep the sub-label and amend A3 to the antecedent rule. Cut it if not.
  - **§4.4 l.4784–4785** "we built the APT attacker model beside MTDSim --- not
    embedded in it" contradicts Marc's 2026-09-24 ruling in the opener (the
    comment above l.4160: "replaces" and "built beside" both wrong; MTDSim runs
    either) and the figure, which draws the two attackers as alternatives in
    MTDSim's Attacker module. A prose fix, Marc's.
  - **§4.4 l.4764** calls the nets "like source code: they have no way of
    running", against the figure's *make executable* (§4.3). Suggested:
    "cannot run against the simulator on their own". Marc's.
  - **The accent changes meaning between Figures 2.1 and 4.1.** In Figure 2.1
    blue marks the attacker's action and path (`tools/ch2_fig21_mtdsim_model.html`,
    undecoded in its caption); in Figure 4.1 blue marks the APT attacker model
    and how it is built (decoded). A reader arriving from chapter 2 carries the
    wrong key. The fix is in Figure 2.1 (neutralise or decode its blue) —
    Marc's file, out of this session's scope.

---

## Part A (primary) — the head figure

**Status 2026-09-25: BUILT** — `tools/ch4_overview_figure.py` →
`fig_4-0a_method_overview` (16.1 × 10.0 cm at \textwidth, smallest type 8.5 pt),
in the tex under `fig:pipeline` as a `[t]` float, caption DRAFT STATE for
Marc's rewrite, build clean (92 pages, no undefined references). It lands at
the top of the page after the chapter's first page (a top float cannot sit on a
chapter's opening page, and the opener leaves too little room for an inline
one), directly after the opener's pointer to it.

| Round | Figure-only reader | With caption | Auditor / critic | What changed after it |
|---|---|---|---|---|
| 1 (two layouts) | 7, 7 | 7 | no blocking; *down* layout over the compact U (the U's leftward *measure* ended the method under its input) | one arrowhead size (heads had scaled with the line); *drives* label; codes $c_1$–$c_4$ dropped (no antecedent), counts drawn one way (card stacks); *hosts and services*; *Petri nets* sub-label |
| 2 | 7 | 7 | caption blocking: *in place of* breaks the 2026-09-24 ruling; *steps* is a taken word | the two attackers drawn as peers with *or* (the ruled "MTDSim runs either"); the join a thin accent step; Figure 2.1's couplings in grey |
| 3 | **8** | 7 | blocking P19: frame "This dissertation" vs the model inside "existing simulator" | frame title dropped, MTDSim "the simulator of Chapter 2", *join to MTDSim*, *interrupts* added, metrics from under the Attacker module |
| 4 | **8** ("would trust it as it is") | 7 | **none blocking** | polish: frame "Building the APT attacker model", "one net per run", blue = the model and how it is built (build arrows blue), *drive* grey |
| 5 (confirm) | **8**, nothing serious | — | — | stop: no reviewer reports a blocking defect |

D1 settled (codes dropped, profiles as a stack); D2 settled (Figure 2.1's
*rewrites*, *compromises*, *interrupts* drawn grey; *observes* omitted);
D3 settled (down; MTDSim's modules mirror Figure 2.1 so the join drops straight
into the Attacker module); D4 settled (no experiment conditions on the figure).

**Content points the readers left for the body text (non-blocking; Marc
dictates):** only one attacker runs at a time, and one profile net per run
(say so where §4.4 opens); the join runs both ways — outcomes return to the
net (§4.4 l.4766; the figure draws it one way, Figure 4.5 carries the return);
the aggregate $c_{\mathrm{agg}}$ also compiles to a net (§4.2/§4.3); bridge the
introduction's *actions* to §4.4's *verbs*; say what "measured" means once
§4.5 is written; the APT attacker model shares the actions but not their
native costs (§4.4.1 l.4813).

**A1. The one message (the pass criterion).** A reader who has read the
introduction, given the figure alone, says: *the 38 attack flows are combined
into one attack graph, split into attack profiles by objective, and each
profile is made executable and joined into MTDSim, where it drives the same
attacker actions as the baseline attacker, against the same defences, and both
are measured.* Every part of that sentence is on the figure; nothing else is.

**A2. Layout: two regions and an output, read left to right.**

```
                ┌──────────── APT attacker model (this dissertation) ─────────────┐
 ▭▭▭            │                                                                 │
 38 attack  ──combine──▶ Attack graph ──split by──▶ Attack   ──make──────▶ Profile│
 flows          │  §4.1                objective   profiles     executable   nets │
 cyber threat   │                        §4.2       c1 c2 c3 c4   §4.3        │    │
 intelligence   └─────────────────────────────────────────────────────────────┼────┘
                                                                         join │ §4.4
                ┌──────────────────── MTDSim (Chapter 2) ─────────────────────▼────┐
                │  Defence              Network              Attacker             │
                │  MTD mechanisms                            baseline attacker ─▶ actions
                └───────────────────────────────┬──────────────────────────────────┘
                                       measure  │ §4.5
                                                ▼
                                      Metrics, per attacker
```

Sketch only: the proportions, and whether MTDSim sits below or to the right
(D3), are decided at the mock. What is fixed:

- **Four groups**, no more (principle H; P8): the input; what this dissertation
  builds (framed); MTDSim (framed as existing); the output.
- **Built vs used is the one grouping the figure makes** (P18, P19): the input
  (the attack flows were drawn by CTID's analysts) and MTDSim sit *outside* the
  built frame; the frame is the APT attacker model. This answers "is MTDSim a
  level?" on the page.
- **MTDSim is drawn as Figure 2.1 draws it**: the three modules *Attacker*,
  *Network*, *Defence*, by those names, so the reader recognises the simulator
  from chapter 2. The baseline attacker lives in the Attacker module (it *is*
  "its procedure" in Figure 2.1); the attacker actions are what both attackers
  drive. No arrows between the modules (Figure 2.1 carries the couplings; D2).
- **Artefacts are boxes, processes are the labelled arrows between them**
  (Wong's "A to B"; P3). The arrow labels are the introduction's verbs:
  *combine*, *split by objective*, *make executable*, *join*, *measure*. Never
  *aggregate*, *condition*, *give executable semantics*.
- **Two arrow kinds only** (P1): *becomes* (the chain, and MTDSim → metrics),
  thin and dark; *drives* (the join into the attacker actions, and the baseline
  attacker into the same actions), visibly different (heavier). Nothing else is
  an arrow.
- **Section pointers under each process arrow** (§4.1 … §4.5), set the way
  Figure 2.1 sets "Figure 2.x" under its modules. They are the navigation into
  the zooms (Part C) and do the job the L-labels did. Chapter 2 under MTDSim.
- **One accent** (Rougier rule 6; P20): the built frame and the join arrow. The
  rest greys. The two-hue exception does not travel here.

**A3. Words.** Every label at most four words. Every word is either one the
introduction gives the reader (attack flows, cyber threat intelligence, attack
profiles, objective, APT attacker model, baseline attacker, MTDSim, defence,
actions) or one the figure defines by boxing it (*attack graph*, *profile
nets*, *join*). Banned on the head figure (P14): *Petri*, *token*, *fire*,
*dwell*, *verb*, *verdict*, *re-weighting*, *runtime loop*, *aggregate*,
*condition*, *semantics*, L0–L4, ATT&CK tactic names.

**A4. No data drawn** (P7, P15): no techniques, no tactic axis, no net marks, no
example flows, no counts except "38" in the input label and the four profile
tiles (the count *is* the fact there). The worked example moves to the §4.1 zoom.

**A5. Caption.** A title sentence and at most one reading sentence; no
"X denotes Y" beyond one (P12; corpus norm 2–9 words, thesis captions run
longer). Session draft for Marc's rewrite, DRAFT STATE:
*"The APT attacker model: built once from 38 attack flows, then run in MTDSim
beside the baseline attacker, under the same defences. Each arrow is labelled
with the section that describes it."*

**A6. Build.**
- New generator `tools/ch4_overview_figure.py`, SVG route per conventions §(n)
  (`tools/ch2_model_figures.py` is the pattern — read it, do not edit it; Marc is
  working in it), printed to PDF through Chromium; house figure face (helvet
  0.92); at \textwidth as a `[t]` float, not a full page. Stem
  `fig_4-0a_method_overview` (conventions §j); **label `fig:pipeline` kept** so
  every `\ref` stands.
- Counts read from the artefacts with a drift guard (38 from the GAP, four
  profiles from the classification), never typed.
- `tools/pipeline_ladder_figure.py` is not deleted: it becomes the source of the
  §4.1 zoom (Part C). Retire the `fig_4-0a_pipeline_ladder` outputs when the
  zoom lands.

**A7. Order of work and the acceptance test.**
1. Mock in the scratchpad (SVG → PNG), two variants if D3 is open (MTDSim below
   vs to the right).
2. `/scrutinise-figure` on the mock, schematic variant: a figure-only cold
   reader and a cold reader with the draft caption (both FRESH), the context
   critic, the diagram auditor on P1–P21. **Pass:** the figure-only reader's
   sentence matches A1 and names the defences, both attackers and the metrics,
   with confidence of 8/10 or better; the auditor reports no blocking hit; every
   word passes A3.
3. Build into the PDF so Marc sees it on the page (his standing rule), replace
   the old float and caption, `FLOATS.md` row, build clean.
4. Re-run the cold readers on the built page; stop when clean.

**Open design details, settled at the mock by the reviewers, not now.**
- **D1 — the profile tiles.** E8 said label by code; a head-figure reader does
  not yet have $c_1$–$c_4$. Try codes with "one per objective" under the box,
  against four short objective names; the figure-only reader decides. The
  aggregate $c_{\mathrm{agg}}$ stays off the head figure (it is §4.2's detail).
- **D2 — arrows inside MTDSim.** Recommended none (containment only). Add
  *rewrites* (Defence → Network) only if the cold reader cannot say what the
  defence does; it is a third arrow kind.
- **D3 — MTDSim below or to the right.** Whichever holds the type floor at
  \textwidth with fewer bends. Below (as sketched) puts the Attacker module
  under the profile nets, so the modules run mirror-wise to Figure 2.1
  (Attacker left there); to the right keeps Figure 2.1's order. Test both.
- **D4 — "with and without defences".** In the caption, or nowhere: the
  experiments are chapter 5's.

## Part B (secondary) — retiring the L-labels

**What the parts are.** Each chapter 4 section describes a *process* that
turns one artefact into the next: combining the flows into a graph, splitting it
by objective, making the profiles executable, joining the net to MTDSim. So
Marc's instinct is right about what the sections are, and the head figure
already draws them that way: the processes are its arrows.

**F4b — what to call them.** *Revised 2026-09-25 on Marc's objection and a
corpus survey.* The first recommendation here — gerund process headings
("Combining the attack flows into an attack graph") — is **withdrawn**: Marc
heard it as storytelling rather than scientific register, and the corpus
agrees. Of 124 method-subsection headings in 29 corpus papers (record:
`../implementation/evaluation_anatomies/_method_heading_survey.md`, locators spot-checked — Alavizadeh 2022
"HARM construction", Zhang 2023 "Modelling Adversary Profiles", Brown 2023
"Defense and Adversary interaction", Cho-Ben-Asher 2018 "Stochastic Petri
Nets"), about 73 % are **noun phrases naming the thing** and 18 % **process
nouns** ("… construction"); gerunds with a different verb per section have no
precedent at this level; numbered "Stage N:" labels appear in one paper. Marc's
own rule already says so: voice.md l.55, "Headings state what the section is
on — nothing more."
- **(a) Recommended — noun-phrase headings, no number, no class noun.**

  | Now | Proposed heading | Form, precedent |
  |---|---|---|
  | §4.1 L0--L1: Cyber threat intelligence to attack graph | Attack graph construction | process noun; Alavizadeh 2022 "HARM construction" |
  | §4.2 L2: Objective-conditioned attack profiles | Attack profiles by objective | noun phrase; drops the coined "objective-conditioned" |
  | §4.3 L3: Generalised stochastic Petri-net formalism | Generalised stochastic Petri-net formalism | noun phrase; the current heading minus the prefix (Cho-Ben-Asher, Alavizadeh head this section by the formalism) |
  | §4.4 L4: Joining the profile net to MTDSim | Integration with MTDSim | process noun; Ferraz 2024, the closest paper. Alternative "The join to MTDSim" keeps the registry noun *join* but reads awkwardly; choosing *Integration* puts a second word beside *join*, which is Marc's to rule |
  | §4.5 Evaluation metrics | unchanged | the corpus's commonest metrics heading |

  The figure's arrows keep the introduction's verbs (combine, split by
  objective, make executable, join, measure) and the headings name the thing;
  the §4.x pointers tie each arrow to its heading.
- **(b) Marc's alternative — "Process 1" … "Process 4".** A numbered name that
  does no work the section numbers do not already do (the 2026-09-22
  no-invented-terms ruling), *process* already appears in chapter 3 as
  *process mining*, and one corpus paper numbers its stages in headings.
- Either way no class noun is needed: every candidate is taken (*phase*: the
  baseline's six and the evaluation's two; *stage*: the lifecycle stages of
  §4.4; *level*: network depth; *step*: Figure 5.1).

**The sweep (after A's names are final, so headings, figure and prose agree).**
Sites, from `grep` 2026-09-25 (non-comment only): the four headings (l.4188,
4298, 4391, 4759); prose l.4269, 4276, 4310, 4400, 4405, 4407, 4698, 4762, 4779,
4989, 5523 (a bracketed placeholder), 7950 (App. B); *levels* meaning the
pipeline's parts at l.4328 ("the prior levels") and l.5182 ("the earlier
levels") — 21 L-label lines in all, five of them the old caption (gone), so
sixteen plus the two *levels*; the fig:pipeline caption
(replaced by A5); **Figure 4.5** — `tools/runtime_loop_figure.py` prints
**L3** and **L4** band labels into `fig_4-4c_runtime_loop.tex`; relabel to the
figure's names (*profile net*, *the join*) and regenerate. Replacement rule:
refer to the artefact or the process by name — "the L1 attack graph" → "the
attack graph"; "from L2" → "from the attack profiles"; "L4 deals with this" →
"the join deals with this"; "Everything from L0 to L3 produces the profile net"
→ "The first three sections produce the profile net". Other `tools/` scripts
use L-labels only in repo-side output (docstrings, stdout, appendix-data
headers) and stay — the registry's scope rule (repo vocabulary may keep them).

**With the sweep:** registry row 47 corrected (L4 is the join; the L-labels
retired, the rule overturned named); the heading-convention memory ("keep L0–L4
prefixes", 2026-09-04) updated; `tools/term_screen.py census` to confirm zero
L-labels in body, headings, captions and floats; build clean.

## Part C (secondary) — the zoom family

**Status 2026-09-25: BUILT** — both new zooms are in the tex (Figures 4.2 and
4.3, `[t]`, captions DRAFT STATE), each through the schematic scrutiny until
clean: the §4.1 figure in three rounds (the blockers: an undecoded top-band
blue; an unscoped 88 %/37 % note that read against the pair gave the opposite
numbers — both fixed; confirmation reader 8/10, "would trust it"), the §4.2
figure in three rounds (the blocker: the caption said each profile was "built
from its own flows", false for the profile as built — fixed to "showing only
the edges its own flows drew"; confirmation reader 8/10). Design departures
the data argued for: the §4.2 figure is a grid of small multiples, not arcs
(122 of 210 tactic pairs, 57 backward); the §4.1 figure ends at the two-flow
combination and hands the full attack graph to the §4.2 figure's first
panel. Revised 2026-09-25 on Marc's read ("a lot of words ... duplication ... the
blue is hard to see"): Figure 4.2 cut to five text items, the shared edges
thick blue labelled "shared", and it now ends on the attack graph itself as a
grid; Figure 4.3 is the four profiles only (2×2), counts in the titles, key cut
to swatches; both captions about 30 words. Fresh cold reads: 8/10 and 7/10,
nothing blocking. Open trade-off: Figure 4.3's bottom row takes its column
names from the shared band above it (a second band costs ~3 cm). Content
points left for the prose: a step between two techniques of one
tactic becomes a self-loop; the assignment rule (by the objective the source
reports record) is also said on the §4.2 figure; the c₁ edge into Impact is
real and not outlined, because the outline is the profile's objective
column.

One figure per part of the head figure, beside the section that explains it,
each using the head figure's name for that part (P17), with the head figure's
section pointer as the link. The house precedent is Figure 2.1 → Figures 2.2–2.4.

| Part (head-figure name) | Zoom | State |
|---|---|---|
| combine (§4.1) | two real flows combined into one graph — the old ladder's L0–L1 half, cut down; the two-hue exception (conventions §i) travels here | **new**, from `tools/pipeline_ladder_figure.py`; its caption re-cites the two flows' reports (`cisaaa22138b`, `malwarebytesadware2018`), which left the bibliography with the old Figure 4.1 caption on 2026-09-25 |
| split by objective (§4.2) | the graph split into $c_1$–$c_4$, the aggregate shown as the unsplit graph; **each row draws its own profile's edges** (the old L2 rows redrew one global set, scrutiny §Also found) | **new** |
| make executable (§4.3) | Figure 4.2, the gadget (`fig_4-3a`) | stands |
| join (§4.4) | Figures 4.3 (tactic-to-verb mapping), 4.4 (failure matrix), 4.5 (runtime loop, relabelled under B) | stand |
| MTDSim | Figure 2.1 and its family, referenced, not redrawn | stands |

Each new zoom gets its own `/scrutinise-figure` pass (schematic variant) and a
`FLOATS.md` row.

*Why new figures rather than reuse (Marc asked, 2026-09-25):* Appendix B's
`fig_B-1a_gap_flow_exemplar` (one flow as the analyst drew it) and
`fig_B-1b`–`d` (the technique- and tactic-level aggregates) are evidence at full
detail — they show what the artefacts *are*, not the process a section
performs, and they stay in the appendix. Chapter 3's
`fig:attack-flow-volt-typhoon` already shows the reader what an attack flow is;
§4.1 can point back to it. The §4.1 zoom (two flows combined) and the §4.2 zoom
(the split) are the two figures that show the processes.

## Part D (carried from 2026-09-22) — the chapter 5 figure fixes

Same generators, small: Figure 5.1 panel (a) in **colour**, a sequential
heat-map fill for the share of steps per tactic (a scoped exception to
greys-plus-one-accent, recorded in conventions §i beside the profile-hue
exception; F2); panel (b) as a **bar chart**, x = opening length in steps, one
colour, y = share of runs that have left the commonest opening (Jin: bars for
proportions, lines for correlated points); Figure 5.2 gains a **key** for the
hollow circles (each mechanism alone) inside the axes. *Added 2026-09-23 (Marc:
"include the baseline, but that's for later"):* Figure 5.1 opens §5.2 *APT
attacker model versus baseline attacker*, so it carries the baseline attacker
beside the profiles, in whatever form panel (a)'s tactic axis allows (the
baseline walks phases, not tactics).

## Validation gate

- **A:** the head figure passes A7 (figure-only cold reader restates A1 naming
  the defences, both attackers and the metrics, 8/10 or better; auditor: no
  blocking hit on P1–P21); built into the PDF; caption within A5.
- **B:** zero L-labels in body, headings, captions and floats
  (`tools/term_screen.py census`); headings, figure arrows and prose use one
  verb per process; registry row 47 and the memory updated.
- **C:** §4.1 and §4.2 have their zooms, each scrutinised clean.
- **D:** Figure 5.1 in colour with panel (b) as bars; Figure 5.2 has its key;
  conventions §i records the exceptions.
- `FLOATS.md` current; build clean. Share with Jin before the week-9 meeting
  (E11).

## Hard constraints

- Figures generated by `tools/` into `docs/thesis/figures/`; Helvetica figure
  face; pack to the page box; never shrink below the type floor.
- `fig:pipeline` label unchanged, so every `\ref` stands.
- No accentuation beyond the encoding; one accent on the head figure.
- Captions session-drafted are DRAFT STATE for Marc's rewrite.

## Reading list

- The scrutiny record below, and `.claude/skills/scrutinise-figure/diagram_best_practice.md` (§2 principles, §4 the tests).
- `docs/implementation/evaluation_anatomies/_overview_figures_survey.md` — Ferraz 2024 Fig. 2, Tay 2024 Fig. 1 (renders in the survey's locators).
- Figure 2.1 (`fig:mtdsim-model`, `dissertation.tex` ~l.561) and `tools/ch2_model_figures.py` (read only).
- The introduction's approach paragraph (`dissertation.tex` ~l.335–354) — the words the figure may use.
- `tools/pipeline_ladder_figure.py` (becomes the §4.1 zoom; keep its drift guards); `tools/runtime_loop_figure.py` (L-labels, Part B).
- `docs/workflows/figure_table_conventions.md` §d, §h, §i, §j, §(n); for D, `docs/handoffs/2026-09-20_ch5_s52_s54_results_context.md` §8b–§8c, §8g.

## Out of scope

Chapter 2's figures (Marc is editing them — `tools/ch2_fig23_*`, `ch2_fig24_*`,
`ch2_model_figures.py` — read, never edit); the chapter 5 effectiveness figures
(the restructure and corpus handoffs redraw them); the formalism's notation
(E9, Marc's).

---

## Scrutiny 2026-09-25 — the evidence for the plan (critique only, nothing redrawn)

*Where this record and the plan above differ, the plan governs (it carries Marc's 2026-09-25 rulings).*

Run with the extended `/scrutinise-figure` (schematic variant; design reference
`.claude/skills/scrutinise-figure/diagram_best_practice.md`, corpus evidence
`docs/implementation/evaluation_anatomies/_overview_figures_survey.md`) on the
figure as built 2026-09-08/-24. Marc's relay of the supervisor (2026-09-25):
still too complicated, labels trying to do too much, not intuitive for the
audience; the long caption gives it away; the levels are not levels — is
MTDSim a level? Four independent reviewers: a cold reader with the caption, a
figure-only cold reader, a context critic, a diagram auditor (P1–P21). Every
claim below was checked against the tex or the generator before acceptance.

**Proposed pass criterion (Marc to agree before any redesign).**
- *The one sentence* (the introduction's approach paragraph, l.~335–354, in
  its words): the 38 attack flows are combined into one graph, split into
  attack profiles by objective, and each profile is executed in MTDSim as the
  APT attacker model, beside the baseline attacker, with and without the
  defences, and measured.
- *The parts*, by kind:

  | Part | Kind | Built or used | Section |
  |---|---|---|---|
  | the 38 attack flows (CTI) | input data | used (CTID's analysts drew them) | §4.1 |
  | the attack graph | derived artefact | built | §4.1 |
  | the attack profiles $c_1$–$c_4$, $c_{\mathrm{agg}}$ | derived artefacts | built | §4.2 |
  | the profile nets | executable artefacts | built | §4.3 |
  | the join (dwell times, tactic-to-verb mapping, failure matrix) | runtime coupling | built | §4.4 |
  | MTDSim: network, MTD mechanisms, the attacker actions, the baseline attacker | existing system | used | ch2 |
  | the metrics | output | defined | §4.5 |

**What every reviewer converged on (blocking).**
1. *It is a worked example, not an overview* (P7): over sixty elements below
   method level; five visual grammars (flow graphs on an axis, merged graph,
   banded rows, a firing net, a message loop); ~24 legend entries against a
   ceiling of about six (P9); two in-figure legends; a 136–142-word caption with
   ~14 decodes and at least five encodings never decoded (the blue frame, the
   ring glyph, the clock, the token box's border, the grey L4 panel) against a
   corpus norm of 2–9 words (P10–P12). The cause of most other hits: remove
   the example and they clear together.
2. *The story is half told* (P21): no defences, no baseline attacker, no runs,
   no measure. Both cold readers named "where is MTD, and what comes out?" as
   the first gap, unprompted. The chapter answers a question about MTD
   performance; the figure stops at a loop with nothing leaving it.
3. *L4 contradicts the chapter*: the figure's gutter and caption say L4 is
   MTDSim (l.4001, l.4010); the §4.4 heading says L4 is the join (l.4759) and
   its first line "Everything from L0 to L3 produces the profile net" (l.4779).
   The registry row 47 records the gutter as *MTDSim*, which is wrong on the
   text's own terms. "join" also names both the arrow into L4 and a box inside
   it.
4. *Terms the reader does not have* (P14): ~16 figure words with no antecedent
   before the figure — *aggregate*, *condition on objective*, *give executable
   semantics*, *Petri net* (0 body uses before ch4), *attack graph* (0),
   *token*, *fires*, *dwell*, *verb*, *verdict*, *re-weighting*, *runtime loop*,
   *double extortion*, *no realised objective*, $c_1$–$c_4$, L0–L4. The
   introduction says *combine* and *split by objective*; the figure says
   *aggregate* and *condition on objective*.

**The two questions the supervisor raised.**
- *Are they levels?* No. L0 is input data, L1–L3 are successive artefacts each
  made from the whole of the one before (a pipeline of stages: Garlan & Shaw
  1994 pp. 6–7), L4 is a runtime coupling, MTDSim an existing system. A layer
  is built on and uses the one below (Garlan & Shaw p. 11; Bachmann et al.
  2000 pp. 11–13); a level is a zoom into more detail (Yourdon §9.3; C4). None
  holds here, and both cold readers read "L" as layer or level, then found the
  figure contradicting it ("L2 is finer again than L1", "L4 is a system, not a
  representation"). *Level* is also ratified for network depth (registry
  row 59). The supervisor's *phase* is taken twice (the baseline attacker's
  six phases; the evaluation's two phases, E1); *stage* is taken by the
  lifecycle stages of §4.4. So no class noun is free, and none is needed if
  the parts are named by what they are.
- *Is MTDSim a level?* No. It is the system the work uses, not a product of
  the chain: the introduction calls it "an existing MTD simulator", §4.4 says
  the model is built "beside MTDSim --- not embedded in it". Drawn as the last
  rung it reads as something the thesis built (P18) — the boundary an examiner
  checks first. The lineage draws the simulator as a container with the new
  part beside it (Tay 2024 Fig. 1 p. 13; Ho 2024 Fig. 1), never as a step.

**Also found.** The grey paths in the L2 rows are the whole graph's twelve
most-observed edges filtered by tactic (`tools/pipeline_ladder_figure.py`
~l.367–405), not each profile's own paths, so the rows draw every profile
alike. Blue carries five meanings (flow A, the thesis's work, the objective,
the token, the firing); the objective ring in L2 is the same glyph as a
marked place in L3. The caption still names and cites the two flows (E8 said
delete). $c_{\mathrm{agg}}$ is absent.

**Sound, and should survive** (the auditor's list, checked): the spine of
noun artefacts joined by verb-labelled arrows (Wong's "A to B" form), with the
introduction's verbs; the stacked-cards glyph for "38 flows" as the input
shape; the plain cardinality lines ("one profile, one net"); top-down or
left-to-right with no reversals; the generator's read-from-artefacts
discipline, which moves to the zooms. The worked example itself is sound
material for the §4.1 zoom (F3).

**Recommended box set (for F1).** Ferraz et al. 2024 Fig. 2 (p. 6) is the
closest corpus match — CTI to executable adversary behaviour: input shape,
stage shapes, output shape, the verbs above the arrows, one accent on the
contribution, the platform not drawn as a step. With the lineage's container:
- left: **38 attack flows** (stacked cards; "cyber threat intelligence")
  → *combine* → **attack graph** → *split by objective* → **attack profiles**
  ($c_1$–$c_4$ as four small tiles, names beside) → *make executable* →
  **profile nets** — the part built once, framed and labelled as such;
- right: an **MTDSim** container (drawn as existing: grey or dashed) holding
  *network*, *MTD mechanisms* and *attacker actions*; the profile nets reach
  the attacker actions through **the join** (the one accent: the APT attacker
  model), the **baseline attacker** reaches the same actions from the other
  side;
- out: **metrics, per attacker** (§4.5).
About four groups (flows; graph and profiles; nets and join; MTDSim and
metrics), one arrow meaning in the chain ("becomes", verb-labelled) and one
across the boundary ("drives"), no legend, and a caption of one or two
sentences. Every part a noun the introduction already uses, except *attack
graph* and *profile net*, which the figure defines by boxing them. Section
numbers under the boxes do the job the L-labels did.

