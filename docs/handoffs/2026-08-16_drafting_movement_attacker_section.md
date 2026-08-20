---
status: open                  # standing context for the §4.2 drafting passes; retire when the section is drafted and scrutinised
created: 2026-08-16
---

# Standing context for drafting "The movement attacker" (methodology §4.2) — the ratified frame, the per-unit speaking framework, and the boundaries

> **Mode note, first.** Marc drafts the prose; sessions scaffold and scrutinise.
> [`../workflows/draft_scrutiny.md`](../workflows/draft_scrutiny.md) governs — a
> session that returns finished dissertation paragraphs has failed, however good
> they are. What a session may return: content-point scaffolds, scrutiny findings
> with grounding documents, and skeleton/figure/citation mechanics.

## State of play

The section's frame was workshopped and **ratified 2026-08-16** (merged to `dev`
at `b4d3ea4`). The skeleton in
[`../thesis/dissertation.tex`](../thesis/dissertation.tex) (`sec:movement-attacker`)
is the authority — its comment blocks carry the full per-unit contract and are
deliberately written as the drafting brief. What was settled:

- **The thesis ladder (Marc's ruling).** The dissertation presents the model's
  *logical* ladder: L0–L1 intelligence→graph, L2 profiles, **L3 = the GSPN
  formalism**, **L4 = the attacker-agent traversal in MTDSim**. Evaluation carries
  **no layer number** — it is the manipulation of the L4 object. This deviates
  from the repo's numbering (repo-L3 = OGASP traversal, repo-L4 = evaluation);
  the divergence is recorded once in
  [`../implementation/architecture.md`](../implementation/architecture.md) §(b).
  **Do not "correct" either document family to the other.** The chapter-opening
  pipeline figure is the definition of the thesis ladder.
- **Four subsections, five units:** L0–L1 (1 unit), L2 (1), L3 (1), L4 (2 — the
  fold of the former Parameterisation + Traversal-and-the-controller units). Any
  subsubsection heading added at drafting is a new unit claim on the writing-guide
  ledger; the L4 fold holds exactly two.
- **Section preamble:** unnumbered, a few sentences, no unit claim. It owes two
  things only — the naming move (*movement attacker* for the proposed model,
  *baseline attacker* for the inherited scripted attacker; V5-consistent) and the
  one-sentence end-to-end orientation (structure → parameters → execution). No
  ladder re-narration: the chapter-opening figure owns the ladder.
- **Placeholder figure** `fig:pipeline` (controller-action PNG) sits at the
  chapter opening until the box-and-flow pipeline figure is drawn to the thesis
  ladder. Caption to be rewritten long and self-contained at the figures pass.

## The purpose of the section, and the framework per unit

**One line: the build told end-to-end, structure → parameters → execution** — how
published CTI became an executable attacker, as simply as the material allows.
Selection discipline: relevant-and-interesting only; the full implementation
record stays in the repo. The problem definition is NOT this section's job
(`sec:requirements` already did it).

| Unit | Question it answers | Must-carry disclosures | Grounding |
|---|---|---|---|
| L0–L1 technique graph | how campaigns become structure | consensus thresholds; what the graph cannot represent | `notes/ch4_methods/technique_graph_construction.md`, `cti_corpus_as_snapshot.md` |
| L2 attack profiles | how structure becomes objective-conditioned | objective over motivation; the four classes; operator concentration | `objective_partition_rationale.md`, `objective_partition_findings.md`, `operator_concentration.md` |
| L3 GSPN formalism | why this formalism | alternatives ranked one sentence each (feasibility study behind it); synthetic pre-intrusion structure; entry-point selection (D8) | `implementation/pipeline/ogasp/petri_feasibility.md`, `stochastic_timing_design.md` |
| L4 traversal (2 units; two subsubsections ruled 2026-08-18: Parameterisation / Mechanics and the join) | what the Petri net cannot supply, and how the net is joined to MTDSim — where the numbers come from + how the net drives the simulator | corpus sparsity; dwell standard-of-evidence; sweep pointer at ch5 (never restated); mapping-as-chosen-input-parameter; routing ablatability | `structure_to_behaviour_binding.md`, `operational_validation.md`, `exponential_as_tractability_choice.md`, `pipeline/ogasp/controller.md` |

The two commitments the L4 fold must not lose (from the 2026-08-12 merge, carried
through the 2026-08-16 fold): **the tactic-to-verb mapping as a chosen input
parameter** (the standing caveat bounding every results-chapter claim) and
**routing ablatability** (null modulator bit-identical to no-modulator).

## Boundaries — questions this section must NOT answer

- **What the simulator is** — ch2 Background (supervisor ruling V7). The preamble
  names the baseline attacker in a sentence; it never re-describes it. The section
  reads as a *backwards join onto the ch2 substrate*.
- **Whether the model is faithful** — ch6's fidelity verdict. The criterion
  subsection before §4.2 poses the yardstick; §4.2 must not pre-claim against it
  (badge ceiling: *designed* stays designed — `apt_model_criterion.md` rules).
- **What the parameters do to outcomes** — the ch5 sensitivity preamble (V6:
  declare, sweep, show movement). §4.2 declares and points.
- **Why the gap exists** — ch3 and `sec:requirements` already earned it.

## Term and heading rulings (from the 2026-08-09 + 2026-08-16 workshopping)

- Sentence case; **no acronyms in headings** (spelled-out forms ratified:
  *cyber threat intelligence*, *generalised stochastic Petri-net*). L-prefixes
  are wanted signage.
- **"Generalised"**, never "general", stochastic Petri net — GSPN semantics
  *executed, not solved* (`stochastic_timing_design.md` §1).
- *Movement attacker* / *baseline attacker* is the ratified naming pair.
- ~~Open micro-flag~~ **Ruled (Marc, 2026-08-16): "attack graph" singular** in the
  L0–L1 heading — applied in the skeleton ("…to an attack graph").

## The drafting pipeline (ratified in practice, 2026-08-16, on L0–L1)

**Promoted to durable:** [`../workflows/drafting_pipeline.md`](../workflows/drafting_pipeline.md)
is now the authority (Marc adopted the pipeline for all future drafting; this
handoff retires with §4.2, the pipeline does not). Summary kept below for
this section's sessions; on any divergence the workflows file wins.

Five drafts per unit; **no pass after draft 1 writes prose** — that is what keeps
the voice Marc's. Sequencing ruling: pilot one unit through all five (L0–L1,
done), then batch drafts 1–2 for the remaining units while warm, then convert
in a run.

1. **Speak** the argument long (aim ~2–3× budget), transcribe raw.
2. **Transcription repair + register 3a** (session task, bundled 2026-08-16 as
   the `repair-dictation` skill — invoke it on any raw transcript): STT errors
   fixed with technical vocabulary watched hardest, disfluencies and pads
   dropped, run-ons split, meta-narration beheaded, hedges flagged as `[3b]`
   markers never resolved; verify watchlist + change log returned. Scrutiny
   rounds run interleaved as `[comments]` (see the scrutinise-draft skill's
   inline-annotated format).
3. **Register pass** (Marc, ~15 min/unit): four Ctrl+F sweeps — pads deleted,
   run-ons split, hedges resolved to confidence or scope, meta-narration
   beheaded. One-touch rule: delete/split/word-repair only, never rewrite a
   sentence; if it needs rewriting, mark `% P5?` and leave. Read-aloud check:
   sounds like Marc being careful, not a journal.
   **Ratified split (2026-08-16):** *3a* (session): detection + pure
   deletion/splits only — pads deleted, run-ons split at conjunctions with
   clause order untouched, meta-narration beheaded where the next sentence
   stands; every hedge flagged as a `[3b]` marker, never resolved; zero
   synonyms, zero reordering. *3b* (Marc): walk the `[3b]` markers (each is a
   binary or a word choice), rule the globals (contractions, second person),
   read aloud. Rationale: deleting Marc's words can't inject a session's; the
   AI-flatten risk lives in repairs-that-choose-words, so those all route to 3b.
4. **Content scrutiny** (session task): `/scrutinise-draft` on the unit, ≤3
   moves. Runs after register, before compression; re-run cheaply if
   compression cuts >half.
5. **Compression** (Marc): per sentence, one binary — "does the unit still
   answer its question without this?" Cut order: duplicates → re-explanations →
   second examples → covered qualifiers. Never cut: must-carry disclosure
   sentences, numbers, citations. Sentence fusion allowed only once cuts stall.

## Validation gate

A unit is done when: (~250 words, 1–2 paragraphs) drafted by Marc; its must-carry
disclosures present as sentences (never new headings); then a scrutiny pass run
under `draft_scrutiny.md` §(b) with the ch4-methods-model pack row, returning at
most three prioritised moves. Voice is Marc's own gate
([`../workflows/voice.md`](../workflows/voice.md)).

## Hard constraints

- No prose generation by sessions (draft_scrutiny §a).
- No renumbering of repo docs/code/data to the thesis ladder (architecture §(b):
  ruled disproportionate).
- Ledger conservation: the section holds 5 units; growth names what it displaces.
- Branch/commit rules per [`../workflows/guardrails.md`](../workflows/guardrails.md).

## Loose threads

- One-line heads-up owed to Jin in the next update: the dissertation's L3/L4 tokens
  now mean formalism/traversal, while the register trail he has been ruling on uses
  L3 = execution model.
- **From the 2026-08-16 L0–L1 drafting passes:**
  - Marc owes a **brief appendix entry** on the co-occurrence preliminary runs
    (single-digit edge counts above a confidence threshold) — it anchors the
    abandonment claim in §4.2.1, which cites it as "Appendix [X]".
  - The **ATT&CK v19.1 pin lost its in-section home** when Marc cut the
    staleness/taxonomy passage from §4.2.1; the pin must surface elsewhere
    (experimental setup is the natural spot) — it is a reproducibility datum.
  - ~~Consensus-thresholds must-carry~~ **Resolved by evidence (2026-08-16):**
    Marc signed the unit off without it, confirming the earlier "not that
    interesting" ruling; the skeleton comment is amended (disclosure list now
    "what the graph cannot represent" only). The lossless/views record stays in
    the repo (`gap_schema.md` Decision 3).
  - **L0–L1 pilot complete through pass 5 (2026-08-16), signed off at ~400
    words.** Open on the unit: the ~1.6-unit ledger overdraft (further cut or
    an explicit named overdraft at the ledger pass); the 80% confidence
    threshold CONFIRM; both appendix entries. **Flag for the L3 drafting:** the
    cycles-preserved sentence was cut from L0–L1 at pass 5, so L3 must
    introduce loop preservation itself — readers default to assuming attack
    graphs are acyclic.
  - **Figure inserted (2026-08-17): `fig:l1-graph`** — three panels on one
    shared tactic axis (one flow as drawn → the 38 flows at technique level →
    the tactic-level aggregate), generated by `tools/l1_attack_graph_figure.py`
    into `thesis/figures/l1_attack_graph.{tex,pdf}`; three panel-keyed
    `(Figure~\ref{...}x)` parentheticals are the only edits to Marc's prose.
    **Owed to Marc:** (i) the caption is session-drafted long-form (writing
    guide step 2) and needs his voice pass, then squeezing as the body absorbs
    it; (ii) the exemplar choice — CISA AA22-138B (TA1) was picked because it
    is small, connected, APT-attributed and carries an AND join; the tool takes
    `--flow` for any other; (iii) the figure spells "Defense impairment" as
    ATT&CK names the tactic — rule whether the thesis Australianises named
    tactics; (iv) the caption states the ATT&CK **v19.1** pin — if that is
    accepted as the pin's home, loose thread (c) above closes. The
    dark-recurring-core / faint-single-incident-tail encoding in panel (b) is
    the 88 % claim drawn; panel (c)'s node sizes are the pre-intrusion
    sparsity (recon 10 / 38, resource development 8 / 38) drawn. The L3
    figure (one profile's net) should reuse the same tactic axis and the same
    grey ramp so the two read as one system.
  - Ruled out of §4.2.1 at drafting, on the record: the Tesla worked example
    (word count), the staleness/map-not-milk passage, the L2 bridge sentence
    (bridges live at the start of each subsection), and — **ruled twice, do
    not re-flag** — the defender-validity argument and the "observability
    boundary" naming (Marc, 2026-08-16: the limitation's "so what" is the
    synthetic pre-intrusion structure, which is the L3 unit's disclosure;
    stating the defence in L0–L1 is premature elaboration. The unit ends on
    the forward pointer; if the term is wanted, L3 or ch6 coins it. This
    supersedes the technique_graph_construction note's ch4 placement of the
    threat-model-input reframe for this unit).
- **From the 2026-08-17 L2 drafting passes (pass 2+3a done; scrutiny run;
  Marc's rulings on the three moves recorded; draft judged "loose", rework
  before 3b/5):**
  - **Membership mechanism — Marc's ruling, do not re-flag:** the chapter tells
    it as *terminal tactic as the primary proxy for objective, cross-checked
    against the CTID blurb, the ATT&CK page and vendor reports*; the audit
    CSV and the "what we actually did" detail move to an appendix. The
    record's inversion (narrative primary; structural terminal the rejected
    P1, 15/38 disagreements — `gasp_schema.md` §(a), D3) stands in the repo
    unchanged; the one open consistency point is that with 15/38 memberships
    decided against the terminal read, the appendix must state the override
    rule or an examiner reading it sees the inversion.
  - **Operator concentration** — Marc excised it deliberately; the disclosure
    is owed (skeleton must-carry). His reframe (same operator → same objective
    across incidents) checks as 5/5 single-G-ID clusters within-class, with
    the Lazarus umbrella and the CISA AA22-138B advisory as the two
    exceptions — `pipeline/gasp/tactic_resolution_restatement.md` §Related.
  - **Tactic resolution** — Marc's ruling: L2 numbers regenerate at
    tactic-to-tactic resolution to match §4.2.1. Done:
    `tools/gasp_tactic_restatement.py` → `pipeline/gasp/tactic_resolution_restatement.md`.
    Carries a **new finding needing his disposition**: the L2 gate's half-split
    null is lenient; under a size-matched label-shuffle null the technique
    separation is at/below p95, tactic-share clears narrowly, transition-share
    does not clear; per-pair, only the impact-present-vs-absent pairs separate.
    The "Jaccard = structurally different" slip is acknowledged (Jaccard shows
    overlap; the discrimination evidence is JSD-vs-null, now null-dependent).
  - Minor rulings: "MITRE deliberately leaves motivation empty" — the record
    holds only "does not maintain" (objective_pivot, Marc's own #13 words) and
    "empty across 187/52 (verified)"; nothing evidences *deliberate* — tidy to
    what the record holds. Retired residual-class labels (pre-positioning /
    infrastructure setup) — Marc: too much, drop. Alternatives (STIX ten
    categories; the seven schemes) — one sentence in the chapter, detail to
    the appendix. Alshamrani phase translation to attack-flow suffix — Marc
    to flesh out.
  - **Corpus thinness at L2 — Marc's ruling (2026-08-17), do not re-flag:**
    the four-class scheme is framed as the chosen balance between corpus
    coverage and class granularity (smallest class five flows); the
    thinness specifics (the ≥2-recurrence collapse, finding 2) are NOT
    broken down in §4.2.2 — §4.2.1 carried the corpus's thinness once, and
    the recurrence-filter lever stays a repo / ch6-limitations point. Only
    leg to keep: the balance claim states its number.
  - **Second scrutiny pass run on the assembled draft (framing/looseness):**
    section verdict rework; the two loose joints (narrative vs terminal
    tactic; "slicing the suffix" vs partitioning whole flows with a shared
    prefix) and the re-ordered closing spine are in the chat return; Marc
    re-dictating long against that spine next.
  - **Fifth pass (2026-08-17, after the inline scrutiny) — Marc's rulings,
    do not re-flag:** motivation sentence reworded to "left unpopulated" (no
    motive imputed; permitted); objective is "evident through the attack
    flows the analysts drew", not the narrative; the chapter's assignment
    story is *composite data* — Attack Flow high-fidelity/low-coverage
    structure, CTI vendor reports for coverage — hence the cross-reference
    and the N-of-38 that move; Alshamrani phase 3–5 names inserted and
    foothold moved to the invariant half (permitted fact fixes); the class
    set stays MITRE-framed (exfiltration / impact / both-in-one-flow /
    neither) — **no Alshamrani/NIST-triad refinement**; the rubric is
    excised (appendix lists the six alternatives and why, no rubric); the
    runtime pre-claim cut and reframed as "capture variably different
    behaviour … for MTD evaluation across a breadth of objectives"; operator
    concentration carried by ONE piece of evidence (half of double extortion
    is Conti, known for it) with the concessions/apology cut; the unit ends on
    the **objective-shaped skeletons** close; **"envelope" is not used** in
    the chapter (Marc: wrong imagery). Two validation handoffs spun out
    (classification confidence / structural baseline; tactic-resolution
    numbers) — the chapter's numbers wait on them.
  - **Sixth pass (2026-08-17, after both validation handoffs shipped and
    Marc's rulings on the second inline scrutiny):** all chapter numbers
    moved to the validated post-ruling set (terminal read 8/12/1 with 19 on
    neither; 19/7/7/5; 19 of 38 under the literal "different category"
    sentence; three of seven Conti); "how much they weight" retired, the
    §8a disclosed-concession sentence carried in Marc's words; the
    Attack-Flow-not-limited-to-ATT&CK expansion carried (smaller of the two
    causes — record flags the truncated-report cause as the larger, Marc's
    call whether named); "in our judgement" ×2 deleted on his "I accept
    that"; scope nouns swapped to "objectives"/"attack profiles". Inline
    flag taxonomy ratified and written into the scrutinise-draft skill.
    **Open for Marc:** the P3 tighten PROPOSAL (accept/deny); "ATT&CK STIX
    data set" (instruction transcribed as "minus 6 stars say 8" — confirm);
    the class-name-follows-definition sentence placement; pass 5.
    **Lingering pre-ruling numbers found:** findings-note body (bannered,
    his) and `operator_concentration.md` l.19 "half of its six" —
    unbannered.
  - **L2 content signed off by Marc (2026-08-17, sixth pass): framing and
    argument right, numbers validated; the two-causes fact-check ruled low
    risk; Appendix~[X]/[Y] stay placeholders until the appendix is wired.
    Pass 5 (compression, Marc) is next; the P3 tighten proposal folds into
    it. Never-cut list and cut order recorded in the session return.**
- **From the 2026-08-17 L3 pre-drafting scan (content-point scaffold returned
  in chat; no prose):**
  - **D8 "both tested" is not on the record as an experiment.** The entry
    toggle exists and is test-pinned (`_choose_entry`: recon seed with the
    overlay on / `initial-access` seed observed-only; `test_petri.py` §7), and
    `demonstration_arms_prereg.md` records "synthetic overlay on — the D8 arm
    every published run uses"; no published run seeds at `initial-access`.
    The skeleton comment's "(D8: both tested)" should read *both testable /
    the comparison arm is a toggle* unless a run is added — `[VERIFY]` before
    it enters prose.
  - **Reversal hygiene on the pack note** `structure_to_behaviour_binding.md`
    (updated 2026-07-13): three positions in it are superseded — the
    capability precondition/effect contract as "the right target" (M4 resolved
    the join shallow: substrate as outcome oracle; S2 froze the action set),
    "timing and success probabilities come from the simulator" (S3-R: the
    movement layer supplies every unit of attacker time), and "envelope, not
    actor" (Marc, 2026-08-17: the word is not used in the chapter). Read it
    for the structure/policy/execution trichotomy and the ontology-gap
    argument only.
  - **Loop preservation has a twist L3 must state:** the L1 graph preserves
    cycles including self-loops (technique_graph_construction: ~37% of edges
    backward, two-thirds of tactics self-loop); the tactic-place nets keep the
    inter-tactic cycles (backward edges are real transitions) but **drop
    intra-tactic self-loops at structural build** — in-tactic time is the
    dwell catalogue's job, not a self-loop weight
    (`data/ogasp/petri/README.md`). So "loops preserved" is true of the walk,
    with self-loops re-expressed as dwell.
- **From the 2026-08-17 L3 drafting passes (pass 2+3a done; 3b walked; pass 4
  inline scrutiny run and Marc's rulings applied — do not re-flag):**
  - **Executed-not-solved / CTMC closed-form vocabulary and the standalone
    analytical track are OUT of the chapter** (Marc: "not critical … not
    something I want to talk about"); the record holds them
    (`stochastic_timing_design.md` §1). Skeleton comment amended.
  - **Alternatives ranked:** one sentence, broad categories only — attack
    graphs/DAGs (acyclic), the other Petri-net forms (SPN puts timing on the
    out-transitions; DSPN not stochastic; closed-form solve not tractable
    because the net re-weights at runtime on the success signal). **No
    appendix** for the data-structure-by-data-structure breakdown; the
    feasibility record stays in the repo. Proposal in the tex from his
    dictation; his SPN reason was heard as "weighted" — written "timing"
    per the record, `[VERIFY]`.
  - **Marking sentence:** Marc keeps his "earliest tactic" framing;
    reconciled with `_choose_entry` (recon with overlay / initial-access
    without; "largest connected component" has no mechanism behind it);
    proposal replaces it with his own dictated form, which doubles as the
    D8 disclosure ("both testable").
  - **Direction:** Marc's ruling — direction is *partly* the net's (the
    out-transitions bound it; the verdict acts on that); trichotomy: net =
    structure only, policy emergent at runtime, execution L4. Proposal in
    the tex.
  - **Wait/weight:** 3b had resolved to "no weight"; ruled — transitions are
    weighted, not timed; base weights insufficient under success/failure →
    dynamic re-weighting later in the pipeline. His "weighting covered at
    L2" corrected to point forward (L4 unit (i)).
  - **Overlay paragraph:** expanded from his dictation (PRE-ATT&CK unified
    into ATT&CK; recon → resource-development → initial-access + backward
    bridge; "nothing detects pre-intrusion activity anyway"); "faithfully"
    deleted (SCOPE). Still open, not dictated: the declared / flagged /
    never-in-the-observed-nets / two-island-profiles leg. `[VERIFY]`
    PRE-ATT&CK merge citation anchor (none in bib).
  - **Self-loops:** insert accepted from his dictation (represented through
    dwell); the sweep-determines-the-curves clause kept out (ch5 pre-claim).
  - **Ceiling paragraph:** framing kept, source split by kind (dwell values
    justified against literature; simulator supplies the success signal) —
    proposal in the tex; "from the literature" flagged against Row A.
  - **Citations:** Marc's hand-verified lit-review `references.bib` (22 May
    2026) merged into `docs/thesis/references.bib` as the primary body
    (his entries supersede same-key repo entries); uncited entries parked
    (commented, at-sign stripped — BibTeX parses `%`-prefixed entries
    otherwise, tested); `mendonca2023` added from the extraction anchor
    and **flagged VERIFY** (not from his verified set); Cai 2016 / Cho &
    Ben-Asher 2018 pending records — Marc will try to obtain Cai (record
    currently: off-limits, second-hand via Mendonça). Precedent sentence
    cites `mendonca2023` only for now.
  - **Draft state (2026-08-17, later):** Marc accepted every proposal; all
    applied as live text (~850 words against ~250 — pass 5 will be heavy;
    the L2-style cut order applies: duplicates → re-explanations → second
    examples → covered qualifiers; never-cut: the alternatives sentence,
    the overlay + entry disclosures, the weighted-not-timed sentence, the
    ceiling paragraph, citations). Open flags left in the tex for his
    rulings: SPN "weighted vs timing" `[VERIFY]`; self-loop "prior stages"
    `[WRONG minor]`; PRE-ATT&CK citation anchor `[VERIFY]`; the overlay
    declared/never-in-observed-nets leg `[INSERT minor]`; "calibrated"
    `[3b]`; the two `[NOTE]` join-word disclosures; the weighting bracket
    (`[covered later in the pipeline]`); Cho & Ben-Asher record; "from
    the literature" `[SCOPE]`; "possibly" `[3b]`. Cai 2016 record obtained
    and cited (label settled GSPN).
  - **Third L3 pass (2026-08-17, Marc's rulings on the open flags):** DSPN
    "not stochastic" fact-checked WRONG (DSPN = deterministic *and*
    stochastic; the record's reason is the periodic MTD trigger living on
    the substrate); SPN objection restated as timing/routing conflation;
    amendment PROPOSAL in the tex with the two record-derived clauses
    starred; formalism cites (Molloy 1982; Ajmone Marsan/Conte/Balbo 1984;
    Ajmone Marsan/Chiola 1987) flagged as anchors to obtain. **All
    subsection facts verified:** 37% backward = 176/478 = 36.8% recomputed
    on gap_v0.5 (15-tactic layer); "up to 15" true only under the v19
    defense-evasion split (stealth/defense-impairment) — the v19.1 pin's
    natural home, flagged; entry rule, overlay edges, self-loops-as-dwell,
    SNAKES build-time, weighted-immediate routing, exponential dwell all
    confirmed against code/record; PRE-ATT&CK merge verified (ATT&CK v8,
    27 Oct 2020) and cited (`mitre2020attackv8`, fetched); Strom 2018
    record verified against the primary PDF (MP180360R1, McLean VA; URL
    replaced with the verified attack.mitre.org locator) — it predates the
    merge, cited for "MITRE has PRE-ATT&CK" only. **Cho & Ben-Asher 2018
    extracted** (`extractions/chobenasher2018.md`, targeted) and cited;
    Cai ruled low-risk by Marc (abstract read). Resolved and deleted:
    sensitivity-determines-curves (ch5, agreed), self-loops "prior
    stages", entry "both testable" note, "calibrated→drawn", "while the
    out-transitions are immediate", executed-not-solved. New proposals in
    the tex: sub-Petri-net overlay clause (his words, record leg
    bracketed); weighting bracket → "covered in the L4 parameterisation";
    ceiling paragraph rescoped (dwell times exist nowhere → inherently
    arbitrary → justified against the literature + ch5 sweep; "to keep
    this project tractable" dropped). Open: the four PROPOSALs; join-words
    `[NOTE]`; formal timed-transitions-not-places `[3b minor]`;
    "possibly" `[3b]`; formalism citation anchors.
  - **Fourth L3 pass (2026-08-17, later):** attack-graphs-acyclic ruling
    withdrawn by Marc (contradicts §4.2.1's cyclic L1 attack graph);
    replacement reason = attack graphs supply no timing/stochastic
    elements; SPN/DSPN ruled out for timing on the transitions; GSPN kept
    for its immediate transitions — **PROPOSAL 2** in the tex from his
    dictation. **No 1980s formalism citations** (Marc: not relevant, not
    interesting) — flag deleted. Applied on his rulings: "Enterprise
    ATT&CK … up to 15~\citep{mitre2026attackv19}" (v19 release note
    fetched and verified: 28 Apr 2026, "Enterprise: 15 Tactics"; the
    v19.1 pin lives in the lit review / background — assumed, not
    restated); the sub-Petri-net overlay sentence with the record clause;
    *pre-intrusion overlay* is the chapter's term for the repo's
    *synthetic overlay* (same object, no re-flag); the "generalised"
    sentence recast on his words (GSPN for its immediate transitions);
    "covered in the L4 parameterisation"; direction join-word note
    removed (accepted); precedent sentence cites the *family* ("for
    stochastic Petri nets"). Open: PROPOSAL 2 (alternatives) and the
    ceiling-paragraph rescope proposal; "possibly" `[3b]`. ~880 words.
  - **Pass-5 ruling (Marc, 2026-08-18, promoted to `drafting_pipeline.md`):
    the first complete pass-5 draft may be well over budget; the cut to the
    ledger is a later refinement over the assembled section. L3 stands at
    ~700 words after the first cut, seven deletion-only tighten proposals
    open in the tex; the ceiling paragraph applied on his confirmed
    ruling. **L4 structure discussed, not ruled:** ratified fold = two
    units; Marc floated three subsubsections (Parameterisation /
    Mechanics / Join to MTDSim) — coherent only on the portability line
    (mechanics = simulator-agnostic walk rules; join = what does not lift:
    tactic→verb table, verdict source, state seam, penalty, bit-identity
    ablation); a third heading is a named overdraft on the ledger.
    **Ruled (Marc, 2026-08-18): two** — the three-way split "not well
    motivated". Written into the skeleton: `\subsubsection{Parameterisation}`
    and `\subsubsection{Mechanics and the join to MTDSim}` under a
    re-framed L4 comment ("what the Petri net cannot supply, and how the
    net is joined to MTDSim"; cross-layer supply may be said in a
    sentence; no fifth rung); L4 heading restored to the ratified "The
    attacker-agent traversal in MTDSim". The earlier "move
    parameterisation into L3" suggestion is superseded.
  - **L3 pass-5 compression written in (Marc's arrangement, 2026-08-18: why
    GSPN > the model > pre-intrusion solution > limits that carry to L4;
    ~330 words live).** Rulings applied, do not re-flag: alternatives head
    restored; "(see sensitivity analysis ch5)" deleted; PRE-ATT&CK head
    dropped as lit-review background — `strom2018mitre` and
    `mitre2020attackv8` are now uncited in the tex but stay active in the
    bib for ch3; "analyst-drawn from L2" stays out (sits badly beside the
    overlay paragraph; L2 carries provenance); the arbitrariness/justified/
    swept sentence leaves L3 for 4.2.4.1. **Three proposals open in the
    tex** (his words): the SPN-not-right-mechanism / DSPN-over-engineered /
    GSPN-in-the-middle clause; the M2 ownership fold (structure only; policy
    emerges through execution = L4) folded into the "supplies the timing"
    sentence so it is said once; the one-sentence M6 justification (nothing
    detects pre-intrusion) — **all three approved and applied 2026-08-18.**
    Ruled: the "generalised" clause not important (out); the one-token AND
    trade-off out of the chapter — a constraint of this work, not the
    formalism; multi-token = **future-work candidate**, recorded in
    `structure_to_behaviour_binding.md` revisit conditions for ch7.
    **Still unruled, minor:** the 37% number; "declared and kept apart from
    the observed profiles". L3 live text ~370 words.
  - **From the 2026-08-18 L4 pre-drafting scan (content-point scaffold
    returned in chat; no prose).** Scaffold order: .1 = L3 obligation
    (arbitrary→justified→swept) > base weights (D3; closed-world +
    recurrence-not-efficacy) > dwell standard of evidence (tiers, four
    anchors, shape-not-scale, S3-R) > exponential-as-tractability (mean
    load-bearing; interrupt-channel leak named as prediction only) > V6
    pointer. .2 = the runtime loop (M1) > mapping as input parameter (S4;
    v2_partial 8/7; host ceiling; standing caveat) > substrate as oracle
    (M4; precondition-unmet and MTD-interrupt read as failure) > direction
    without a stage machine (M2/M3; success/failure asymmetry; anti-fitting
    rule; adversarial review + lifecycle-distance constraint) > sink retrace
    (S5) > confusion penalty stays on the border > attacker-only seam
    (D5/M7, beside-not-inside) > routing ablatability (null = bit-identical).
    **Flags for Marc:** (1) placement of the overlay *values* (.1 family vs
    .2 mechanism; V6 sends the table to an appendix); (2) `[VERIFY
    wording]` Tier-1 post-S3-R — magnitudes still *sourced from* substrate
    constants (scan 35 = 5+5+25; exploit 4.5 median) though no longer
    *charged* by it on the movement arm; (3) `[SCOPE]`
    operational_validation's Tier-2 "calibrated" vocabulary is aspirational
    (catalogue v0-uncalibrated; R1 sequenced calibration post-MVP) — chapter
    says declared→justified→swept only; (4) `[SCOPE]` whether experiment-1
    numbers (sink censoring 74–210 vs ~500 actions; v1 mapping's friction/
    churn) may motivate S4/S5 in §4.2.4 or stay ch5; (5) `[3b]`
    interrupt-as-failure at the routing verdict vs host_simulator_contract's
    "interrupt distinguishable from failure" — routed alike, recorded apart;
    (6) host_simulator_contract.md positions itself for an "implementation
    chapter" that no longer exists — portability is one sentence at most,
    ceiling "priced, exercised on one host"; (7) if the recon→impact zero is
    cited, it is inert on this corpus (no three-stage transition exists) — a
    defensible-parameter result, not behavioural.
  - **L4 pass 2+3a done (2026-08-19, repair-dictation):** Marc's dictation
    repaired into the tex under his ruled split (preamble + Parameterisation +
    Mechanics and the join; the beside-not-embedded / runtime-instrumentation
    point folded into the preamble from his follow-up dictation). ~1,100
    words against the 2-unit ~500 (within the speak-long 2--3x aim). Nine
    `[3b]` markers + one `[figure slot]` open in the tex. Verify watchlist
    returned in chat --- highest-value repairs: "from the original simulator"
    self-correction resolved to "from the movement layer" (base weights);
    "not suspicious"->"not sufficient"; "22nd"->"20-second confusion
    penalty"; "defend a sportsy"->"the defender thwarts the". Two NEW
    appendix debts dictated: the dwell-time derivation table ("see the
    appendix") and the full tactic-to-tactic weight sets (V6 already routes
    the overlay matrix to an appendix). 3b walk is Marc's; then
    /scrutinise-draft runs pass 4.
  - **L4 pass 4 run and Marc's rulings applied (2026-08-19), do not
    re-flag:** timeline-dead-end expansion, beside-MTDSim reframe, preamble
    tighten, closed-world sentence, exponential non-claim, mapping-as-input
    sentences, forced-total-mapping reconciliation (VERIFIED: v1_ckc_total
    tried, experiment-1 friction/churn --- the #16 rejection was the separate
    replace-the-FSM idea), overlay paragraph reworked (15-by-14 no
    self-loops; stages preparation / intrusion / post-intrusion operations /
    objective; citations wired: hutchins2011 + mandiant2013 added to the
    bib, chemat2024 unparked; Ussath cited via Alshamrani). **Routing
    ablatability must-carry CUT by Marc** (skeleton comment amended; the
    guarantee stays repo-side, ch5 cites attacker_state_seam.md). **Open in
    the tex:** the kernel [WRONG] (declared kernel does NOT penalise one
    stage away --- his narrative does; his "that's how it should be done" =
    candidate re-declaration, provenance handoff carries it); the left-out
    "we swept them" Q&A line (declare-then-sweep boundary); the
    self-driving-framing [3b]; closed-world assumption-status [3b minor];
    stochastic-nature citation slot; the sec:sensitivity pointer; M2's
    read-never-re-rolled insert (unruled). **Figure slots ruled:** the
    runtime data-flow loop (primary figure of the subsection, drawn after
    polish; spec in the tex comment) and the four-phase overlay diagram
    (placeholder). **For sec:experimental-setup:** mapping-swap as an
    experiment dimension (Marc's ask). **Pass-5 candidates he floated:**
    the 45 s / 0 s worked examples ("not strong"); the doubled zero-or-one
    constraint sentences. **Two handoffs spun out:**
    2026-08-19_failure_only_overlay_feasibility.md and
    2026-08-19_failure_weight_provenance.md (his decomposition idea:
    failure kernel x distance kernel -> aggregated matrix) --- the owed
    failure-encoding paragraph waits on them.
    **Feasibility handoff shipped (2026-08-19):** record
    `implementation/pipeline/ogasp/success_null_overlay_feasibility.md` —
    success column priced by a 4 000-run ablation (profile-signed 1–3 host
    effect, no headline moved; kernel-only third arm ruled out on
    expressiveness: loses the foothold gate, stalls a profile).
    **RULED 2026-08-19 — failure-only adopted** ("having a success matrix
    makes no sense logically"): `v4_failure_only` registered as the
    go-forward overlay (v3's failure table; success = the corpus
    proportions, unconditioned); `v3` frozen under the published records.
    **Consequences for the tex:** the §4.2.4 dictation's "15-by-14 failure
    and success matrices" and "if the attacker succeeds, we're overlaying
    the success tactic-to-tactic weight set" describe the retired
    configuration — Marc re-dictates that half (one declared matrix, on
    failure; on success the token routes on the corpus proportions, which
    already encode what successful campaigns did next); `success_weight_matrix`
    drops out of ch4; the owed failure-encoding paragraph is unblocked.
    Content points in the record's §9; the published ch5 numbers stay on
    `v3` unless the re-key ruling (README) says otherwise.
    **Provenance handoff shipped and retired (2026-08-19), on Marc's
    split:** ch4 gets the committed matrix (`fig:failure-weight-matrix`,
    rule letter in every cell; `success_weight_matrix` generated too for
    the keep-the-pair case), the appendix gets the decomposition
    (`fig:failure-weight-decomposition`) + the declared point in its sweep
    bands (`fig:distance-kernel-bands`) + the rule-ledger / kernel / full-set
    tables — all by `tools/failure_weight_decomposition_figure.py`. The
    §4.2.4.2 content-point scaffold, the three wiring blocks
    (compile-checked; **not applied** — Marc verifies first) and the
    where-every-number-lives table are in
    `implementation/pipeline/ogasp/failure_weight_decomposition.md` §5.
    The kernel `[WRONG]` closed with his flag walk (`bdf3de7`); the M3
    floor-semantics flag on that paragraph remains his to word (the bands
    figure draws the correct semantics).
  - **L4 flag walk (2026-08-19, later) --- rulings applied, do not
    re-flag:** the self-driving framing DELETED (Marc: a conflation, he
    misspoke --- no replacement); closed-world named as an assumption
    (minimal fix "We assume that ..." applied; a PROPOSAL sentence from his
    corpus-bound dictation open in the tex); the why-GSPN dictation folded
    into the exponential block (stochastic behaviour needs a capability;
    exponentiation provides it; base dwells are not stochastic) --- the
    definitional "measured but not predicted" claim re-affirmed by Marc, its
    [3b] dropped; the kernel narrative FIXED to the record values on his
    fix-and-simplify ruling (1 / 1 / 0.25 / floor 0.1 -> exactly 0) with the
    floor explained in his words; the swept-line stays out (ruled: the sweep
    defends, it does not produce); **the sweep pointer goes to the APPENDIX,
    not ch5** ("the sweep is not as interesting") --- note: V6 put swept
    parameters in a results preamble; if an examiner-facing tension appears
    it is Marc's to reconcile; a sweep-wiring handoff is a MAYBE (his "leave
    that as a handoff as well"), owed when the appendix is built; the M2
    read-never-re-rolled point REMOVED on his ruling (what it was, for the
    record: M4's rule that the verdict is read from the substrate's own
    outcome, never re-rolled --- stays repo-side in controller.md section 4).
    **New idea under exploration (his concurrent session + the feasibility
    handoff's third arm): failure encoded purely as asymmetric kernel decay
    (backward decays differently) --- one mechanism; the destination-aware
    foothold gates are what it cannot express** — now measured:
    `success_null_overlay_feasibility.md` §5.8 (4–11 % vs 65–83 % back to
    reconnaissance on a failed initial access; the adjacent form stalls
    `objective_exfiltration` in 47/160 runs). Still open in the tex: the
    closed-world PROPOSAL; the stochastic-nature citation slot; the kernel
    sentence's reword-freely note; pass-5 overlap notes.
  - **L4 second flag walk (2026-08-19, after the v4 adoption) --- rulings
    applied, do not re-flag:** S3-R dictated in (the movement layer supplies
    all attacker timing at runtime; same-verb-different-time from the
    invoking tactic --- "different" inferred, [3b] in the tex); the GSPN
    re-tell TIGHTEN agreed (cut at assembly); the stochastic-nature sentence
    ruled "tacked on" by Marc --- HIS re-dictation owed, anchors all wired
    (holm2014 + madan2004 ADDED to the bib from extraction metadata,
    mcqueen2006 unparked, bland2020 already active); judged-best-fit mapping
    dictation in (three restatements now --- pass-5 note); forced-total-
    mapping reason in (tightly ordered FSM run unordered-but-stochastic;
    Appendix~[X] = experiment-1 record --- NEW appendix debt) with the
    foreshadowing sentence carried under a [SCOPE minor] (ch5 pre-claim;
    sanctioned form = the #24 pre-registered expectation); floor sentence
    corrected on his sanction (floor tests the kernel value at fold-in);
    anti-fitting dictation in with a [3b] on its direction (his spoken form
    inverts the record's boundary); **adversarial-review defence ruled OUT
    of the chapter** (an AI-scrutiny methodology point); the
    knowledge-and-real-world-data sentence placed at the L4 subsection
    preamble close (note in tex: move if the SECTION preamble was meant);
    the pending failure-paragraph slot replaced by a PROPOSAL block of
    content points from the shipped success_null_overlay_feasibility.md
    section 9 (both 2026-08-19 handoffs closed by the concurrent session;
    v4_failure_only adopted --- the success-half sentences still carry that
    session's re-dictation flag). dissertation.tex left UNCOMMITTED: the
    concurrent session has in-flight section-preamble hunks in the same
    file; whoever commits next carries both.
  - **Appendix debts now three:** co-occurrence preliminary runs (§4.2.1);
    the audit CSV polished + membership rule (§4.2.2); the candidate-scheme
    comparison (§4.2.2).
