# ch2_background — notes feeding the Background chapter

## What this chapter does

The background chapter (ch2 in the ratified structure, between the introduction and
the literature review) carries **the two existing things this thesis builds on**: the
moving-target-defence vocabulary the rest of the document speaks, and the inherited
simulator it runs on. Existing things, presented for comprehension — the ruling that
moved the simulator out of the methodology and into a background chapter of its own
(supervisor register V7, 2026-08-11: it "is not methodology — it describes existing
things"). The arguments *about* these components — the comparability boundary, the
baseline's fairness, the scoring of its threat model — belong to ch3 and ch4; ch2
describes and hands over. (Whole-document guidance:
[`../_writing_guide.md`](../_writing_guide.md).)

**Scope widened, 2026-08-21.** The chapter was originally platform-only. The
moving-target-defence concept material — attack surface, *what / how / when*, the
shuffle–diversity–redundancy family, the trigger regimes — was re-homed here from
the literature review, on V7's own criterion: it too describes existing things, and
the review's contract (each work told as method → limitation → next, narrowing onto
the gap) has no room for vocabulary that narrows nothing. The full reasoning trail,
the port map from the submitted review, and the rulings on every candidate live in
[`../../handoffs/2026-08-21_ch2_background_context.md`](../../handoffs/2026-08-21_ch2_background_context.md)
— read it before proposing any change to this chapter's shape.

## The two placement tests

Both were derived in the 2026-08-21 workshop and both will keep recurring, so they
are stated here rather than left in the handoff that will be retired:

1. **Ch2 carries the terms and artefacts the document *uses*; ch3 carries the claims
   the document *argues against*.** Register, not topic. Definitional and descriptive
   here; evaluative and narrowing there.
2. **Ch2 carries what is *inherited*; ch3 earns what is *chosen*.** MTDSim arrived
   with the lineage and no alternative was weighed, so it is described here. Attack
   Flow won an argued two-option trade against automated extraction, so it is earned
   in ch3 and used in ch4 — putting it in background would make the review's best
   passage read as retrospective justification.

A structural consequence worth knowing: this thesis **inherits its defence side and
builds its attacker side**, so these tests return *yes* for MTD-side material and
*no* for CTI-side material with some regularity. Ch2 describing MTD but not CTI is
that asymmetry showing through the structure, not an omission in it.

## The structure

Ratified shape (Marc, 2026-08-21). **1 250 words / 5 units** (writing guide ledger;
ch2 was cut 6→5 on 2026-08-12 to fund the methodology's 11-unit skeleton). Five
heading-claims against five units — the ledger is untouched and neither float unit is
spent, so any new heading still has to name what it displaces.

| Heading | Job | Words |
|---|---|---|
| *(chapter opener, unnumbered)* | the frame, two sentences | ~60 |
| **2.1 Moving target defence** | attack surface; *what / how / when*; shuffle–diversity–redundancy; proactive / reactive / hybrid | 250 |
| **2.2 MTDSim** *(preamble)* | what the simulator is, then the lineage in two sentences over **Table 2.1** | ~120 |
| 2.2.1 Network model | topology, host and service structure, exposure | 250 |
| 2.2.2 Defence mechanisms | the roster wearing 2.1's labels; the execution schemes; the reactive selector | ~300 |
| 2.2.3 Attacker model | the scripted six-phase attacker, its two scenarios, its exploit ordering | 250 |

**Why it nests.** A flat four-section version was proposed first and rejected on
altitude: it put *Moving target defence* — a field — at the same heading level as
*Network model*, one component of one simulator. The nested shape is also closer to
V7 than the pre-2026-08-21 skeleton, since V7 names exactly three components
(network model, defence model, procedural attacker) and they are exactly the three
subsections. Folding the chapter opener and the retired *Prior work* section into a
single §2.2 preamble is what frees the words §2.2.2 needs.

**§2.1 — the field, and the discipline that keeps it here.** Cited to Cho 2020, with
the premise anchored to the field's NITRD origin (`ghosh2009nitrd`); Hong 2018 no
longer appears here — its metric-partition material followed the inherited suite to
ch4/ch3 under the 2026-08-21 metrics ruling. **It surveys no works.** The
moment it starts naming papers and their limitations it has become ch3, and the fix
is to cut, not to balance. Its job is to make ch3 readable: §3.2 (*attacker models in
MTD*) and §3.3 (*how MTD is evaluated*) both presuppose a reader who knows what a
shuffle is and where a trigger regime sits, and nothing else in the skeleton teaches
that.

**§2.2 — the artefact.** The preamble says what MTDSim is (a discrete-event simulator
over a three-layer HARM) and narrates only the *shape* of the lineage's evolution;
Table 2.1 does the enumerating. Per-work narration is deliberately cut — everything
that matters about each work is described where it is used, with attribution riding
as a clause (*the execution schemes Zhang added*) rather than as a section. This is
the "describe once" discipline: Brown's attacker and Tay's agent are described
*here* and referred back to from ch3, never re-described there.

**§2.1's vocabulary must earn its keep inside §2.2.2**, in that unit's first two
sentences, or it was decoration: the simulator carries **shuffle and diversity only —
no redundancy** ([`../../implementation/substrate_primer.md`](../../implementation/substrate_primer.md)
§(c) states this as an honest scope note, and ch6 leans on it), and its operations
sort by **which layer of terrain they mutate** — position versus surface — which is
the reading ch4 and ch5 actually use and which needs the *what to move* question
posed first.

### Table 2.1 — placement and columns

**Placement: under §2.2, in the preamble.** It is a property of the artefact, not of
the chapter, and floats sit outside the word budget — which is why the lineage
survives at full strength while its prose section does not.

**Three columns: *work* / *what it added* / *what this thesis inherits*.** The third
is the one that earns the table a place; the first two alone are a related-work list,
which is the thing ch2 is not. Indicatively: Brown 2023 (MTDSim over a three-layer
HARM, combined-MTD evaluation) → the platform, network model and scripted attacker;
Zhang 2023 (the time domain, MTTC, the MTD execution schemes) → the schemes as
§2.2.2's *when*, MTTC as the primary metric; Ho 2024 (the extended metric suite) →
the supplementary measures, described in ch4; Tay 2024 (the reactive DDQN selector) →
the selector used as-is, retraining ruled out (V3).

**Condition booked from §2.2.1's compression (2026-08-27, cut C7):** the Brown row's
*what it added* cell must carry that Brown extended Alavizadeh et al.'s two-layer HARM
with a service layer — the attribution was cut from the prose on the condition that
the table carries it.

Rows are what each work **added to this codebase**, not what each paper contributed
to the field — those diverge, and the field-level headlines (Zhang shuffle-dominant,
Ho diversity-dominant) are V5's comparison points for the evaluation, not ch2's.

Three later passages lean on the table, which is why cutting the lineage section did
not cut it: ch4's comparability boundary presupposes four studies over one evolving
codebase; ch5's first experiment family re-runs the lineage's own published
evaluations; and a thesis extending three prior students' code needs one visible
place where inherited and built are separated.

### Deliberately absent

- **The inherited metric suite → ch4 §4.3.2.** `dissertation.tex` already gives
  `subsec:metrics` "the inherited suite and its comparability boundary"; describing
  it here as well made three metric touches in the document. §2.2.3 keeps one
  forward-pointing clause.
- **Attack Flow and ATT&CK → ch3 §3.1.** Test 2 above. Flow objects are ATT&CK-keyed,
  so admitting one drags the other, and ATT&CK's ch3 job (the durability argument
  licensing technique-and-tactic-level modelling) is argumentative and cannot follow.
  §2.2.3 may name the kill chain and ATT&CK as attribution for the inherited
  attacker's design, with a forward pointer — a background chapter may name a
  framework it does not teach. *Reopening condition:* if drafting §4.2.1 (L0→L1)
  needs ~150 words explaining what a flow object **is** before the construction can
  be described, the fix is two definitional sentences in ch3 §3.1.3, not a ch2
  section.
- **No pipeline figure.** The ladder belongs to ch4's opening. Ch2 carries one
  float of its own besides Table 2.1: **Figure 2.1**, the three-module model
  diagram in the §2.2 preamble (ruled 2026-08-27; generator
  `tools/mtdsim_model_figure.py`, plan
  [`../../handoffs/2026-08-27_ch2_model_diagram_plan.md`](../../handoffs/2026-08-27_ch2_model_diagram_plan.md)).
  It frames the three subsections and pre-installs the layer-landing reading
  (shuffles rewrite the network layer, diversity the host layer) ch4 and ch5 use.
- **No gap talk, no lineage headlines, no fidelity verdicts.** All three are other
  chapters' and spending them here spends them twice.

### Still open

**§2.2.2 dictation context (2026-08-27):** the unit's academic context, refreshed
for the seven-mechanism pool and the distinct OS diversity, is
[`../../handoffs/2026-08-27_ch2_defence_mechanisms_context.md`](../../handoffs/2026-08-27_ch2_defence_mechanisms_context.md)
— read it with the two 2026-08-21 briefs before scaffolding; every record dated
before 2026-08-27 describes the four-mechanism, OSD-equals-SD state.

**How much network model the document needs — answered 2026-08-27.** §2.2.1 is
drafted (dictated, passes 2–5 run, 264 words against 250) and carries exactly what
ch4/ch5 lean on: the three layers, the generators, depth and the fixed ingress, priced
and synthetic vulnerabilities, and the visible subgraph (the reset model's premise).
Preconditions, the targeted scenario and the behaviour-binding forward clause were cut
as not leaned on. Voice gate and the forward-use test against Figure 2.1 are pending
the figure's wiring.

### State of `dissertation.tex`

**The tex has not been restructured.** It still carries the pre-2026-08-21 skeleton —
four `\section` blocks (prior work / network model / defence mechanisms / attacker
model) and a `sec:lineage` label. Cutting it to the shape above is a separate
ratified pass: four sections become two, three subsections nest under the second, and
`sec:lineage` disappears (verify nothing `\ref`s it first). Until that pass runs,
**this file is the authority on ch2's shape and the tex is not.**

## What lands here

Prose that explains the inherited platform and the vocabulary — at the altitude a
reader needs to follow the rest of the dissertation. The technical detail a reader
would need the repo to follow stays in [`../../implementation/`](../../implementation/)
(the substrate primer, the metrics semantics, the boundary records); a note earns a
place here only when the *explanation* is itself dissertation prose. Rubric-gated
([`../../workflows/notes_rubric.md`](../../workflows/notes_rubric.md)).

One standing discipline against this chapter's failure mode, which is bloat:
**nothing enters that a later chapter does not lean on.** If ch4 and ch5 never refer
back to it, it is not background, it is a manual.

**Placement note (2026-08-14):** the gap-statement and precedent-survey notes that
previously sat here moved to [`../ch3_lit_review/`](../ch3_lit_review/) when the
background and literature-review chapters were separated — those are the literature
review's *occupying move* (naming and narrowing onto the gap), not descriptions of
the inherited platform. Expect most background notes to arrive when the chapter is
drafted; until then the platform's technical record lives in `implementation/`.
