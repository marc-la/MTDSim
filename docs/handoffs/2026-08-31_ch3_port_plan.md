---
status: open                  # the executing brief for the ch3 boil-down; retire when the ch3 skeleton is cut into dissertation.tex and every portable unit is assembled
created: 2026-08-31
supersedes-in-part: 2026-08-21_ch3_lit_review_design.md (Part 2's unit ledger and section order; Part 1's contract stands)
amended: 2026-09-02 — §2's within-strand order revised on Marc's ruling (see the amendment note atop 2026-08-31_ch3_patchwork_draft.md): 3.2 runs opener → metrics → evaluation methods (renamed) → hinge as unnumbered closer; 3.3 runs interstitial → traditions → criterion → cross-section → gap. Ledger and gaps unchanged.
---

# Porting the literature review into ch3 — Marc's working plan critiqued, the ruled-on shape, the section-level port ledger, and the gaps that have to be written

> **Mode note.** Marc's 2026-08-31 ask: an MVP draft of the dissertation, fast,
> so the polishing time is spent on the polish. For ch3 that means the same
> method that produced §2.1 in one session — **assemble the review's own
> audited sentences into the new shape** (the ch2 port ledger's
> verbatim / adapted / cut discipline) and leave a visible `[GAP]` marker
> wherever the review has nothing to port, for Marc to dictate. Sessions
> assemble and scrutinise; the gaps are Marc's dictation. Nothing here is a
> sentence for the chapter.

Companions: [`2026-08-21_ch3_lit_review_design.md`](2026-08-21_ch3_lit_review_design.md)
(Part 1 — what the chapter owes the document — stands in full; Part 2's ledger
and order are revised below), the retired scrutiny brief
(`git show c03231b4:docs/handoffs/2026-08-21_lit_review_scrutiny.md` — the
per-section verdicts and the four-mechanism diagnosis of why §IV reads weak),
[`../notes/ch3_lit_review/README.md`](../notes/ch3_lit_review/README.md),
[`../implementation/apt_model_criterion.md`](../implementation/apt_model_criterion.md)
§(a) and §(c) (the instrument the cross-section will now be scored on), and
the ch2 port method in
[`2026-08-21_ch2_background_context.md`](2026-08-21_ch2_background_context.md)
Part 3.

---

## 1. Marc's plan, point by point

Marc's proposal (2026-08-31): a short preamble; §3.1 the APT survey built from
§III-C, §III-D, §III-A; §3.2 how MTD is evaluated, built from §II-B's metric
work alone; §3.3 attacker models in MTD, moved last, opening on the Cho 2020 /
Jalowski 2026 interstitial, then 3.3.1 the eight axes derived from the
literature, then 3.3.2 the recent works graded against them. Five verdicts.

**(a) Model last — adopt.** The design brief argued capture → model → evaluate
as a dependency order, but its own scrutiny follow-up revised the gap's spine
from *evaluation altitude* to *fidelity* (scrutiny §(d)). Once fidelity is the
spine, the chapter's closing claim *is* the model strand's verdict, and the
strand carrying the closing claim should close the chapter. The dependency the
brief worried about (the reader cannot see the evaluation gap until they accept
that the attacker model bounds the metric) is satisfied inside the evaluate
strand itself, which now ends on exactly that hinge and hands it to §3.3. The
resulting order reads: *here is what a real campaign looks like* → *the
evaluation machinery is mature, but every metric is scored over an attacker*
→ *the attacker it is scored over is thin; here is the rubric; here is the
scoring; here is the gap.* This reorders a ratified skeleton (V5's three
sections, 2026-08-11) — Marc's structure to rule, recorded as CONFIRM 1 below.

**(b) The eight axes derived in ch3 — adopt, with a boundary, and it costs
a ruling.** Marc's instinct fixes the one thing the review's §IV could not fix
by editing: it carries two instruments (Cho's four characteristics plus the
fidelity ladder in Table II; the eight axes everywhere else in this project).
An examiner who meets a four-column table in ch3 and an eight-row scorecard in
ch6 has been handed two yardsticks and will ask which one the thesis believes.
One instrument, derived once, used three times — prior work in ch3, adopted as
the yardstick in ch4, this model in ch6 — is the coherent document. It also
answers the scrutiny brief's second diagnosis ("the instrument is asserted, not
earned"): earning a rubric *from the literature* is literature-review work, and
§III-D already shows what an earned instrument looks like in this review.

The boundary that keeps ch4's opening move intact: ch3 §3.3.1 establishes the
axes **as the literature's characterisation of a sophisticated attacker** —
what Cho names, what NIST's clauses add via Alshamrani, what Jalowski's
corrective adds — numbered 1–8 in the criterion's order (the numbers are cited
across the record and are never renumbered). Ch4 §4.1.2 then **adopts** them as
the yardstick: the badge vocabulary, the anti-reverse-fitting provenance (axes
fixed before the model was scored), the lettered rows A/B, and the
pose-never-score discipline. The derivation is ch3's; the epistemic discipline
is ch4's. This inverts design-brief rule 4 and the "not pose the fidelity
criterion" boundary — CONFIRM 2 — and has two mechanical consequences: the
§4.2 preamble's shipped `\ref{sec:requirements}` for "the axes" re-points to
the ch3 label, and §4.1.2 shrinks to roughly half a unit, which is the natural
answer to the §4.1 brief's open CONFIRM 1 (Marc's own dictation queried
whether §4.1 needs two subsections at all): fold §4.1 to one unit, problem
definition plus adoption of the yardstick, and return a unit to the ledger.

**(c) §3.1 from III-C, III-D, III-A — adopt the content, fix the order.** III-D
(attack profiling) cites Attack Flow as its manual strand, and Attack Flow is
introduced in III-A; III-D cannot precede III-A. The order that is both
chronological and a dependency chain is: what an APT is (III-C) → the
vocabulary its campaigns are recorded in (III-A: ATT&CK, then Attack Flow) →
the method that reconstructs behaviour from the record (III-D). The design
brief's re-aim (CONFIRM 1 there: the strand surveys *the behavioural record and
what it does and does not carry*, not the threat groups) is the frame that
makes those three port cleanly, and it supplies the strand's closer for free
from an existing note: the artefacts encode sequence, not duration.

**(d) §3.2 from II-B only — adopt.** §II-A is already in ch2 §2.1 (ported
2026-08-21); §II-B's MTDSim/HARM paragraph became ch2's lineage table; §II-C's
one payload — the asymmetry sentence — survives as a single sentence, placed
once (see the ledger). What II-B carries into ch3 is the validation ladder,
Table I, and — repurposed — its game-theoretic paragraph, which is not
evaluation material at all but the seed of the model strand's *strategic
attacker* unit.

**(e) The preamble — tailored, not condensed.** The review's introduction is
built on the Pyramid of Pain frame (apex / base), which the scrutiny brief
retired on two grounds (its direction is uncited and arguably inverted on
Bianco's own terms; it welds model fidelity onto a ranking of indicator
classes). Condensing it would carry the frame in. What survives from §I is the
two-literatures-developing-without-converging paragraph (minus the pyramid
clause) and, used once in the whole chapter, the signature line ("the defender
has grown more sophisticated; the adversary against which it is evaluated has
not"). What replaces the rest is the design brief's scissors — two blades and a
missing hinge — the three strands keyed to their sub-questions, and the
selection rule (first / most established / latest). No research question
restatement (ch1 owns it) and no "the remainder is structured as follows".

## 2. The shape — 12 units, 3 000 words

| Heading (working title) | Job | Units | Source | Port status |
|---|---|---|---|---|
| *(preamble, unnumbered)* | the scissors; strands keyed to sub-questions; selection rule; the coverage claim planted | 1 | §I ¶2 (adapted, pyramid clause cut); design brief "rhetorical shape" | **mostly new** |
| **3.1 Survey of APT attackers** | *capture* — can the literature hand you a machine-usable behavioural specification of a campaign, and what does it still not carry | 3 | | |
| 3.1.1 What makes the campaign different | three-property definition, NIST clauses, five-phase lifecycle with its objective-conditioned suffix, the commodity contrast; long-dwell and objective-driven evidenced from current reporting | 1 | §III-C ¶1–2 (tighten); *latest* slot from the macro-timing extraction (M-Trends 2026 median dwell, espionage split) | portable + **gap (latest slot)** |
| 3.1.2 The behavioural record | ATT&CK to its origin and version; the durability argument (Sadlek, not Bianco); ATT&CK-in-STIX records *which*, not *how*; Attack Flow supplies order and dependency; the analyst-curated corpus. **Figure 3.1**: the Tesla flow (review Fig. 2) | 1 | §III-A whole; §III-B ¶2 only (Sadlek durability); | portable |
| 3.1.3 From reports to structure | attack profiling; manual curation vs automated extraction priced on coverage vs fidelity; the SoK plateau; the methodological commitment to curated input. Closer: the record encodes order, never tempo | 1 | §III-D whole (the exemplar — port nearly verbatim); closer from `tactic_duration_precedent_survey.md` ("Corpora and emulation frameworks: sequence yes, timing no") | portable |
| **3.2 How MTD is evaluated** | *evaluate* — the instruments are mature, and every one of them is scored over an attacker | 3 | | |
| 3.2.1 The ladder of methods | the four validation categories; why simulation dominates; what each rung can and cannot support (the pros/cons Cho tabulates — ch4 positions on this ladder and owns simulation's cons) | 1 | §II-B ¶1 + ¶4 | portable + **gap (~half: the per-rung cost sentence)** |
| 3.2.2 The metric suite | Cho's perspective × purpose partition; Hong's network-state-dynamic extension. **Table 3.1** (= review Table I) | 1 | §II-B ¶3 + Table I | portable |
| 3.2.3 What the metrics are scored over | the hinge: ASP, MTTC, the path measures — each is computed against an attacker's progress, so the attacker model is not an input to the evaluation but a bound on it; the asymmetry sentence lands here, once | 1 | §II-C last ¶ (one sentence) | **gap** |
| **3.3 Attacker models in MTD** | *model* — the field says so about itself; the rubric; the scoring; the gap | 5 | | |
| *(3.3 interstitial, unnumbered)* | Cho 2020 and Jalowski 2026 name the attacker model as the field's primary limitation, six years apart — two sentences, then the surveys "stop at diagnosis" and the strand measures | ½ | §IV-A compressed to its two sentences (scrutiny: "cut to two sentences") | portable |
| 3.3.1 What the literature says a capable attacker is | the eight axes derived: Cho's four characteristics and three under-developed dimensions, the NIST clauses via Alshamrani, Jalowski's scheme-awareness corrective; the fidelity ladder **earned** — why four rungs, why that order, where the boundaries fall | 1 | §IV-B ¶1–3 (the four characteristics, the ladder's rung list); criterion §(a) for the derivation trail | portable + **gap (earning the rungs, ~100 w)** |
| 3.3.2 How the field has modelled its attacker | chronological: the probabilistic / attack-graph default → the game-theoretic strategic attacker (sophisticated in interaction, empty in behaviour) → learned attackers; Bland and Outkin as proof the components of a sequencing, cost-aware, engagement-parameterised attacker exist and have never been brought to MTD | 1 | §II-B ¶2 (game-theoretic, repurposed); §V ¶2–3 (Bland, Outkin — moved up from the synthesis, per scrutiny §(i)) | portable + **gap (the default and learned rungs, ~120 w)** |
| 3.3.3 What recent work actually assumes | **Table 3.2**, the cross-section scored on the eight axes plus the ladder rung; one paragraph led by rhetoric-versus-execution (ATT&CK and the kill chain invoked as framing, absent from the executed threat model); the adverse-sample warrant; He et al. in prose as the adjacent contrast case | 1½ | §IV-B ¶4 and the five per-paper subsections, compressed to the table plus one paragraph; He et al. subsection → two prose sentences | portable (compression) |
| 3.3.4 The demonstrated need | the three strands closed: the behaviour is capturable (3.1), the instruments cannot see past the attacker model they are scored over (3.2), the models never leave the scripted rung (3.3) — and the consequence: a threat model at that rung cannot represent a campaign past initial access, so MTD's performance against a footholded adversary is unmeasured *because of* the fidelity ceiling. Names what would have to be built; stops | 1 | §V ¶1 (the "rationality without capability" close, once); the coverage consequence argued, not surveyed | portable + **gap (the closing move, ~100 w)** |

Arithmetic: 1 + 3 + 3 + (½ + 1 + 1 + 1½ + 1) = 12. The interstitial is not a
heading and draws no unit of its own; it and the table paragraph share 3.3's
five units.

**What the ledger changes against the design brief:** 1 / 3 / 4 / 4 becomes
1 / 3 / **3** / **5** with the strands reordered. The evaluate strand gives up
its fourth unit ("what the instruments presuppose" — the pre-foothold-adversary
claim the scrutiny brief showed is absent from the review and never evidenced
against the literature) to the model strand, where the eight-axis derivation
now sits. The coverage claim survives as 3.3.4's consequence sentence, which is
where the fidelity-spine ruling put it.

## 3. The two tables and one figure

Floats sit outside the word budget and are drawn *before* their units are
assembled (writing guide order of operations).

- **Table 3.1 — the metric families.** Review Table I, re-keyed to the bib
  (`cho2020`, `hong2018`). Genre: comparison table with citation column
  (conventions §e2). The inherited suite's *definitions* (equation, direction)
  stay in ch4 §4.3.2 under the 2026-08-21 metrics ruling; ch3 catalogues
  families and cites origins, it does not define.
- **Table 3.2 — the attacker-model cross-section on the eight axes.** This is
  the chapter's strongest evidence and the artefact an examiner looks for. Two
  design decisions, both Marc's:
  1. *Cells are phrases, not ticks.* Review Table II failed because 18 of 20
     cells were ✗ (scrutiny §(b)3); on eight axes the ratio worsens. The
     criterion's own "prior MTD work" column already holds the phrases
     ("partial RoA ordering over scanned exploits"; "design-time threshold,
     swept"; "—") — the table is that column transposed, one row per work, so
     it *measures* where the field has anything and is honestly empty where it
     has nothing. The conventions' ✓-matrix genre (§e1, empty cell not ✗) is
     the fallback if the phrase cells will not fit the page.
  2. *Rows.* Recommend **one lineage row** (Brown 2023 / Zhang 2023 / Ho 2024 /
     Tay 2024) in place of the review's separate Brown and Tay rows: ch2's
     Table 2.1 has already established that four works share one attacker, and
     a single row makes the asymmetry claim — the defender advanced across four
     works, the attacker never moved — visible in the table itself. Tay's
     IDS-sensitivity sweep, the one attacker-adjacent experiment in the
     lineage, is a clause in the row's adaptivity cell. Then Masud 2025, Kim
     2026. **He et al. leave the table** (scrutiny §(c): by the review's own
     concession the attack class does not transfer; as the only row with ticks
     it contaminated the sample) and return as the prose contrast case.
  3. *The same table returns in ch6* with one row added — the movement
     attacker — as the fidelity verdict's visual. Ch3's copy carries no row for
     this thesis (design brief boundary: cite nothing of this work's own).
- **Figure 3.1 — the Tesla cryptojacking flow** (review Fig. 2). The review's
  one concrete worked example, which the marker's feedback asked for. It
  illustrates the capture *apparatus* as literature, so it lands in 3.1.2;
  ch4 §4.2.1 must not carry a second flow figure (the ch2 README's reopening
  condition already routes "what a flow object is" to ch3). Regenerate from
  the review's TikZ under the thesis figure pipeline (12pt, greys plus one
  accent, keyed to its landing per conventions §j).

## 4. The gaps — what the review cannot supply

In priority order by how much of the chapter's argument each carries. All are
Marc's dictation; a session may stage a noun-stub cue card per gap from the
grounding named.

| # | Gap | Where | Size | Grounding available |
|---|---|---|---|---|
| G1 | **The hinge**: each metric is computed over an attacker's progress, so the attacker model bounds what any of them can express | 3.2.3 | 1 unit | `cho2020` (attacker-side metrics defined over attack outcomes), `hong2018` (APV/APN/APE computed over attack paths — over the attack-graph's attacker assumptions), `mttc_lineage.md` (MTTC over compromise events) |
| G2 | **The closing move**: fidelity → coverage as consequence; what would have to be built; stop | 3.3.4 | ~½ unit new (rest ports from §V ¶1) | scrutiny §(d) (the fidelity-spine ruling); `post_ingress_mtd_gap.md` for the *argument* only — its survey-level citation anchors are unreconciled and must not be asserted |
| G3 | **Earning the ladder's rungs**: why parametric / scripted / procedural / behavioural, why that order, where each boundary falls | 3.3.1 | ~100 w | criterion §(e) (the descriptor is Marc's own instrument — flagged as this project's synthesis, never a paper's claim); the per-paper placements in §IV-B are the boundary cases |
| G4 | **The default and learned attacker** (the probabilistic / attack-graph tradition; RL attackers as reward-shaped exploration over an abstract state space) | 3.3.2 | ~120 w | `rl_security_environments.md`, `chobenasher2018.md`, `bland2020.md`, `outkin2023.md`; `hongkim2012harm` / `hongkim2016` for the graphical-security-model default |
| G5 | **The APT strand's *latest* slot** — the review's §III-C rests on one 2019 survey and names Volt Typhoon uncited | 3.1.1 | 2–3 sentences | `breach_reports_macro_timing.md` (M-Trends 2026 median dwell 14 d; espionage 122 d — verified against primary); `cisaaa22138b` is already in the bib; a Volt Typhoon advisory needs a bib entry (to add, Marc's list) |
| G6 | **The per-rung cost sentence** for the ladder of methods | 3.2.1 | ~½ unit | `cho2020` Table VI (pros and cons per validation method) |
| G7 | **Citation repairs** — the Cyber Kill Chain cited to `hutchins2011` where the phase vocabulary is introduced; NIST's APT clauses cited to NIST rather than via Alshamrani (bib entry to add: NIST SP 800-39, verify); ATT&CK to `strom2018mitre` with the version pin inherited from ch4 | throughout | mechanics | extractions on file; scrutiny §(f) |

Not gaps, because staged notes already carry them: the sequence-not-tempo
closer (3.1.3, from `tactic_duration_precedent_survey.md`) and the durability
argument (3.1.2, Sadlek via §III-B ¶2).

## 5. What the review carries that the chapter refuses

- The **Pyramid of Pain** as frame, Fig. 3, and every "apex" / "base" clause
  (abstract, §I, §III-B ¶1, §IV-A, §IV-B, §V). Bianco may survive as a single
  attribution if the durability sentence wants it; the argument stands on
  Sadlek without him.
- **§IV-A's two paragraphs** beyond its two sentences (a subsection functioning
  as a runway).
- The **conclusion stated three times** (§IV-A ¶1, §IV-B-6, §V ¶1): one
  statement, at 3.3.4.
- The **signature line twice**: once, in the preamble or at 3.2.3, never both.
- The **research question and the approach** (§V-A, §V-B): ch1 and ch4 own
  them; the review's RQ predates the capture / model / evaluate decomposition
  and must not be ported as written (scrutiny §(i)).
- **§II-C's orchestration survey** (Masud's conflict rules; Tay's DDQN): Masud
  returns in the cross-section, Tay is ch2 lineage; the rest is double-counted.
- **Five phase vocabularies**: the chapter affords two — ATT&CK tactics as
  working vocabulary, the kill chain named once as lineage — plus the ladder,
  visibly distinguished as an instrument rather than a phase model.
- **Forward pointers closing paragraphs** (15 of 84 in the review): the
  chapter's units close on their own claim.

## 6. Method for the assembly session

The ch2 §2.1 port is the template and it worked in one session: a sentence
ledger (`S1 … Sn`, source line in `LIT_REVIEW.md`, verbatim / adapted / cut,
the ruling each adaptation rides), decisions batched for Marc (em-dash policy,
example trimming, the signature line's single placement), the voice §(f) gate
run at insertion, `% DRAFT STATE` comments carrying the port and the pending
items. For ch3, run it **one section per session** in reading order — 3.1
(most portable, lowest risk), then 3.2, then 3.3 (most compression, and the
two tables must exist first) — with each gap left as a visible
`\emph{[GAP Gn --- …]}` placeholder carrying its grounding pointer, so the
assembled chapter reads end to end with its holes labelled. Marc dictates the
gaps through the pipeline; pass 6 runs once per section after the last gap
closes.

Two things the assembly must not do: compose sentences the review does not
contain (the gaps are Marc's), and touch `dissertation.tex` while Marc has it
dirty in another session — check `git status` first and coordinate.

## 7. Open CONFIRMs — Marc's calls before the skeleton is cut

1. **Section order.** Capture → evaluate → model, model closing the chapter.
   Reorders V5's ratified three-section sequence; the labels and the
   sub-question keying are unchanged. *Recommended: adopt.*
2. **The eight axes derived in ch3 §3.3.1, adopted in ch4 §4.1.** Inverts
   design-brief rule 4 and the "not pose the criterion" boundary; re-points
   the §4.2 preamble's `\ref{sec:requirements}` to the ch3 label; folds §4.1
   to one unit and returns one unit to the ledger (the §4.1 brief's CONFIRM 1
   answered in the same stroke). *Recommended: adopt.* The alternative — keep
   two instruments and reconcile them in a sentence — is the review's §IV
   problem carried into the thesis.
3. **Table 3.2 design**: phrase cells over ticks; one lineage row; He et al.
   out; the same table returning in ch6 with this model's row. Four
   sub-decisions, ruled together.
4. **The ledger split** 1 / 3 / 3 / 5, and 3.3.4 numbered rather than an
   unnumbered closing block (the chapter's most important paragraph should
   appear in the contents).
5. **Figure 3.1's home** — ch3 3.1.2 (recommended) or ch4 §4.2.1, never both.
6. **The signature line's single placement** — preamble (recommended: it is
   the scissors in one sentence) or 3.2.3.

## Validation gate

The skeleton is cut into `dissertation.tex` with a budget comment per unit;
Tables 3.1–3.2 and Figure 3.1 exist under the figure pipeline; every portable
unit is assembled from ledgered review sentences; every gap G1–G7 is either
dictated or a labelled placeholder; the chapter builds; the design brief and
this file are deleted in the commit that ships the last section.

## Reading list for the assembly session

1. This file, then the design brief's Part 1.
2. The retired scrutiny brief (`git show c03231b4:docs/handoffs/2026-08-21_lit_review_scrutiny.md`).
3. `docs/sources/lit_review/LIT_REVIEW.md` (the quarry; gitignored) — §III-A,
   §III-C, §III-D, §II-B, §IV-B, §V ¶1–3 are the portable regions.
4. `2026-08-21_ch2_background_context.md` Part 3 — the port method.
5. `apt_model_criterion.md` §(a), §(c), §(e); `voice.md` §(f);
   `literature_conventions.md` §a, §d, §f.
